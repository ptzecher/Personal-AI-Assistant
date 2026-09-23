class Agent:

    def __init__(self,llm):
        self.llm=llm

    async def run(self,message):
        response=await self.llm.generate(message)

        return response