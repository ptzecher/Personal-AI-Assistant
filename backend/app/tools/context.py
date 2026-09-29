from contextvars import ContextVar

current_db=ContextVar("current_db")
current_user_id=ContextVar("current_user_id")