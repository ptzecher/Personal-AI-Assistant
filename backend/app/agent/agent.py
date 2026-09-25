from database.repository import *
from sqlalchemy.orm import Session

from agent.tools import calculator


class Agent:

    def __init__(self,llm):
        self.llm=llm
        self.tools={
            "calculator":calculator
            }



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
        llm_response=await self.llm.generate(history)

        if llm_response["type"]=="text":
            final_answer= llm_response["content"]
            save_message(db,conversation_id,"assistant",final_answer)

        elif  llm_response["type"] == "tool_call":
            tool_name = llm_response["name"]
            tool_args = llm_response["args"]

            if tool_name not in self.tools:
                raise ValueError(f"Unknown tool: {tool_name}")

            print(f"Executing {tool_name} with {tool_args}")

            tool=self.tools[tool_name]

            result=tool(**tool_args)

            print(f"Tool result:{result}")

            response = await self.llm.generate_with_tool_result(
                contents=llm_response["contents"],
                model_response=llm_response["model_response"],
                tool_name=tool_name,
                result=result
            )

            if response.function_calls:
                raise RuntimeError(
                    "Additional tool calls are not supported yet"
                )

            final_answer = response.text
            save_message(db,conversation_id,"assistant",final_answer)
            

        else:
            raise RuntimeError("Unexpected LLM response")

        if not final_answer:
             raise RuntimeError("Gemini returned no final answer")
    
        return final_answer
        

        

        

     
