from google import genai
import os
from dotenv import load_dotenv

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

        response= await self.client.aio.models.generate_content(model=self.model,contents=contents)
        return response.text
    

