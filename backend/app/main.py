from fastapi import FastAPI,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from agent.agent import Agent
from llms.base import LLM
from pydantic import BaseModel
from database.database import get_db
from sqlalchemy import text
from sqlalchemy.orm import Session
from database.repository import *
from schemas.conversation import *
from schemas.auth import *
from auth.security import hash_password,verify_password,create_access_token
from auth.dependencies import get_current_user


app=FastAPI()


llm=LLM()
agent=Agent(llm)


class ChatRequest(BaseModel):
    conversation_id: int
    message: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/chat")
async def chat(request: ChatRequest,
               db:Session=Depends(get_db),
               current_user: User = Depends(get_current_user)):

    conversation=get_conversation(db,request.conversation_id)
    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    if conversation.user_id!=current_user.id:
        raise HTTPException(status_code=404,detail="You cannot access this conversation!")
    

    try:

        response=await agent.run(db=db,message=request.message,conversation_id=request.conversation_id)

        return{
        "response": response
         }
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

@app.get("/get_db")
async def db_test(db:Session=Depends(get_db)):

    result = db.execute(text("SELECT 1"))

    return{
        "database":result.scalar()
    }

@app.post("/test_db")
async def database_test(db: Session = Depends(get_db)):
    user=create_user(db,"pantelistze@gmail.com")

    conversation=create_conversation(db,user.id,"Favourite Porgramming Language")

    save_message(db,conversation.id,"user","Hello Gemini, my favourite programming language is python.")
    save_message(db,conversation.id,"assistant","Got it — I’ll remember that Python is your favorite programming language.")
    

    messages=get_messages(db,conversation.id)

    return{

        "user_id": user.id,
        "conversation_id":conversation.id,
        "messages":[
            {
                "role":message.role,
                "content":message.content
            }
            for message in messages
        ]
    }


@app.post("/conversations",response_model=ConversationResponse)
def create_new_conversation(conversation:ConversationCreate,
                            db:Session=Depends(get_db),
                            current_user: User = Depends(get_current_user)):

    new_conversation=create_conversation(db,current_user.id,conversation.title)

    return new_conversation


@app.get("/conversations",response_model=list[ConversationResponse])
def read_conversations(db:Session=Depends(get_db),
                       current_user: User = Depends(get_current_user)):

    conversation_list=get_conversations(db,current_user.id)
    return conversation_list



@app.get("/conversations/{conversation_id}",response_model=list[MessageResponse])
def read_conversation_msgs(conversation_id:int,
                           db:Session=Depends(get_db),
                           current_user: User = Depends(get_current_user)
                           ):

    conversation=get_conversation(db,conversation_id)

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    if conversation.user_id!=current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You cannot access this conversation"
        )

    return get_messages(db,conversation_id)

@app.patch("/conversations/{conversation_id}",response_model=ConversationResponse,
           )
def update_conversation_title(conversation_id:int,
                              data:ConversationUpdate,db:Session=Depends(get_db),
                              current_user: User = Depends(get_current_user)
                              ):

    conversation=get_conversation(db,conversation_id)
    if conversation is None:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found"
            )
    
    if conversation.user_id!=current_user.id:
        raise HTTPException(
            status_code=403,
                detail="You cannot access this conversation"
        )

    updated_conversation=update_conversation(db=db,conversation_id=conversation_id,title=data.title)

    return updated_conversation

@app.delete("/conversations/{conversation_id}")
def delete_conversation_endpoint(conversation_id:int,db:Session=Depends(get_db),
                                 current_user: User = Depends(get_current_user)                          
):


    conversation = get_conversation(
        db,
        conversation_id
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    if conversation.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You cannot delete this conversation"
        )

    delete_conversation(db=db,conversation_id=conversation_id)

    return {
        "message":"Conversation deleted succesfully"
    }

@app.post("/auth/register",response_model=UserResponse,status_code=201)
def register(data:UserRegister,db:Session=Depends(get_db)):

    existing_user=get_user_by_email(db,data.email)

    if existing_user is not None:
        raise HTTPException(status_code=409,
                            detail="Email already registered")

    hashed_password=hash_password(data.password)

    user=create_user(db,data.email,hashed_password)
    return user


    
@app.post("/auth/login",response_model=TokenResponse)
def login(
        form_data:OAuth2PasswordRequestForm=Depends(),
        db:Session=Depends(get_db)
):
    user = get_user_by_email(
        db=db,
        email=form_data.username
    )
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    password_valid = verify_password(
        form_data.password,
        user.hashed_password
    )

    if not password_valid:
        raise HTTPException(status_code=401,detail="Invalid email or password!")
    access_token=create_access_token(user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

