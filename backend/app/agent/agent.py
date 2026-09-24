from database.repository import *
from sqlalchemy.orm import Session


class Agent:

    def __init__(self,llm):
        self.llm=llm



    async def run(self,db:Session,conversation_id:int,message:str):

        conversation=get_conversation(db,conversation_id)

        if conversation is None:
            raise ValueError("Conversation Not found")

        save_message(db,conversation_id,"user",message)

        messages=get_messages(db,conversation_id)

        history = [
            {
                "role": msg.role,
                "content": msg.content
            }
            for msg in messages
        ]
        response=await self.llm.generate(history)

        save_message(db,conversation_id,"assistant",response)

        return response
