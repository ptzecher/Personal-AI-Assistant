from tools.registry import ToolRegistry
from tools.calculator import calculator
from tools.weather import get_weather

tool_registry=ToolRegistry()

tool_registry.register("calculator",calculator)
tool_registry.register("get_weather",get_weather)


