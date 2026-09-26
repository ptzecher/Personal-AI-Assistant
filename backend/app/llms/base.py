from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

from tools import tool_registry

load_dotenv()


class LLM:

    def __init__(self):
        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

        self.model = "gemini-3.5-flash-lite"

    def build_contents(self, messages):

        contents = []

        for message in messages:

            role = message["role"]

            if role == "assistant":
                role = "model"

            contents.append(
                
                types.Content(
                    role=role,
                    parts=[
                        types.Part(
                            text=message["content"]
                        )
                    ]
                )
            )

        return contents

    async def generate(self, contents):

        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=contents,
            config=types.GenerateContentConfig(
                tools=tool_registry.get_all(),
                automatic_function_calling=
                types.AutomaticFunctionCallingConfig(
                    disable=True
                )
            )
        )

        if response.function_calls:

            function_call = response.function_calls[0]

            return {
                "type": "tool_call",
                "name": function_call.name,
                "args": dict(function_call.args or {}),
                "model_response": response.candidates[0].content
            }

        return {
            "type": "text",
            "content": response.text
        }