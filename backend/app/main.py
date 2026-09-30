from fastapi import FastAPI,Depends,HTTPException
from agent.agent import Agent
from llms.base import LLM
from pydantic import BaseModel
from database.database import get_db
from sqlalchemy import text
from sqlalchemy.orm import Session
from database.repository import *
from schemas.conversation import *



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
async def chat(request: ChatRequest,db:Session=Depends(get_db)):

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
def create_new_conversation(conversation:ConversationCreate,db:Session=Depends(get_db)):
    user_id=8

    new_conversation=create_conversation(db,user_id,conversation.title)

    return new_conversation


@app.get("/conversations",response_model=list[ConversationResponse])
def read_conversations(db:Session=Depends(get_db)):
    user_id=8

    conversation_list=get_conversations(db,user_id)
    return conversation_list



@app.get("/conversations/{conversation_id}",response_model=list[MessageResponse])
def read_conversation_msgs(conversation_id:int,db:Session=Depends(get_db)):
    user_id=8

    conversation=get_conversation(db,conversation_id)

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    if conversation.user_id!=user_id:
        raise HTTPException(
            status_code=403,
            detail="You cannot access this conversation"
        )

    return get_messages(db,conversation_id)

@app.patch("/conversations/{conversation_id}",response_model=ConversationResponse)
def update_conversation_title(conversation_id:int,data:ConversationUpdate,db:Session=Depends(get_db)):

    user_id=8
    conversation=get_conversation(db,conversation_id)
    if conversation is None:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found"
            )
    
    if conversation.user_id!=user_id:
        raise HTTPException(
            status_code=403,
                etail="You cannot access this conversation"
        )

    updated_conversation=update_conversation(db=db,conversation_id=conversation_id,title=data.title)

    return updated_conversation

@app.delete("/conversations/{conversation_id}")
def delete_conversation_endpoint(conversation_id:int,db:Session=Depends(get_db)):
    user_id = 8

    conversation = get_conversation(
        db,
        conversation_id
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    if conversation.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You cannot delete this conversation"
        )

    delete_conversation(db=db,conversation_id=conversation_id)

    return {
        "message":"Conversation deleted succesfully"
    }
    

