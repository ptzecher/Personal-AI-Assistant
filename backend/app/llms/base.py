from google import genai
import os
from dotenv import load_dotenv
from google.genai import types
from agent.tools import calculator

load_dotenv()


class LLM:


    def __init__(self):
         self.client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

         self.model = "gemini-3.5-flash-lite"

    async def generate(self,messages):
        contents=[]
        for message in messages:
            role=message["role"]
            if role=="assistant":
                role="model"

            contents.append({
                "role": role,
                "parts": [
                    {
                        "text": message["content"]
                    }
                ]
            })

        response= await self.client.aio.models.generate_content(model=self.model,
                                                                contents=contents,
                                                                config=types.GenerateContentConfig(tools=[calculator],
                                                                                                   automatic_function_calling=types.AutomaticFunctionCallingConfig(
                                                                                                       disable=True
                                                                                                   )),
                                                                )
        print("FUNCTION CALLS: ",response.function_calls)

        if response.function_calls:
            function_call=response.function_calls[0]

            return {
                "type": "tool_call",
                "name": function_call.name,
                "args": dict(function_call.args or {}),
                "contents": contents,
                "model_response": response.candidates[0].content
            }
        
        return {
    "type": "text",
    "content": response.text
}

    async def generate_with_tool_result(self,contents,model_response,tool_name: str,result):
        contents = [
            *contents,
            model_response,
            types.Content(
                role="user",
                parts=[
                    types.Part.from_function_response(
                        name=tool_name,
                        response={"result": result}
                    )
                ]
            )
        ]

        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=contents,
            config=types.GenerateContentConfig(
                tools=[calculator],
                automatic_function_calling=types.AutomaticFunctionCallingConfig(
                    disable=True
                )
            )
        )

        return response
        

