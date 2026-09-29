from tools.registry import ToolRegistry
from tools.calculator import calculator
from tools.weather import get_weather
from tools.web_search import web_search
from tools.create_note import create_note
from tools.search_notes import search_notes

tool_registry=ToolRegistry()

tool_registry.register(tool_name="calculator",function=calculator)
tool_registry.register(tool_name="get_weather",function=get_weather)
tool_registry.register(tool_name="web_search",function=web_search)
tool_registry.register(tool_name="create_note",function=create_note)
tool_registry.register(tool_name="search_notes",function=search_notes)

