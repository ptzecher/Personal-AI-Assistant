from fastapi import FastAPI
from agent.agent import Agent
from llms.base import LLM
from pydantic import BaseModel



app=FastAPI()


llm=LLM()
agent=Agent(llm)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/chat")
async def chat(request: ChatRequest):
    response=await agent.run(request.message)

    return{
        "response": response
    }