from database.repository import *
from sqlalchemy.orm import Session

from google.genai import types

from tools import tool_registry


class Agent:

    def __init__(self,llm):
        self.llm=llm
        self.tools=tool_registry



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

        contents = self.llm.build_contents(history)



        llm_response=await self.llm.generate(contents)

        MAX_ITERATIONS=5

        

        for _ in range(MAX_ITERATIONS):

             # -------------------------
            # NORMAL TEXT RESPONSE
            # -------------------------

            if llm_response["type"] == "text":

                final_answer = llm_response["content"]

                if not final_answer:
                    raise RuntimeError(
                        "Gemini returned no final answer"
                    )

                save_message(
                    db,
                    conversation_id,
                    "assistant",
                    final_answer
                )

                return final_answer

            if llm_response["type"] != "tool_call":
                raise RuntimeError(
                    "Unexpected LLM response"
                )

            tool_name = llm_response["name"]
            tool_args = llm_response["args"]


            # Make sure the requested tool exists
            if self.tools.get(tool_name) is None:
                raise ValueError(
                    f"Unknown tool: {tool_name}"
                )

            print(
                f"Executing {tool_name} "
                f"with {tool_args}"
            )


            # Execute the actual Python tool
            result = self.tools.execute(
                tool_name,
                tool_args
            )


            print(
                f"Tool result: {result}"
            )

            # -------------------------
            # ADD TOOL CALL TO HISTORY
            # -------------------------

            contents.append(
                llm_response["model_response"]
            )


            # -------------------------
            # ADD TOOL RESULT TO HISTORY
            # -------------------------

            contents.append(
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_function_response(
                            name=tool_name,
                            response={
                                "result": result
                            }
                        )
                    ]
                )
            )

            # -------------------------
            # ASK GEMINI AGAIN
            # -------------------------

            llm_response = await self.llm.generate(
                contents
            )

        raise RuntimeError(
            "Maximum number of tool calls exceeded"
        )