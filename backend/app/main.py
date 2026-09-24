from fastapi import FastAPI,Depends,HTTPException
from agent.agent import Agent
from llms.base import LLM
from pydantic import BaseModel
from database.database import get_db
from sqlalchemy import text
from sqlalchemy.orm import Session
from database.repository import *



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


