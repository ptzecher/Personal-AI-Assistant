class ToolRegistry:


    def __init__(self):
        self.tools={}


    def register(self,tool_name:str,function):
        self.tools[tool_name]=function

    def get(self,tool_name):
        return self.tools.get(tool_name)

    def execute(self,tool_name:str,args:dict):

        tool=self.get(tool_name)

        if tool is None:
            raise ValueError(f"Tool {tool_name} does not exist")

        return tool(**args)

    def get_all(self):

        return list(self.tools.values())

    
