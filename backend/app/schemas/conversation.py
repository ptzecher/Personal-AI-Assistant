from pydantic import BaseModel,ConfigDict
from datetime import datetime

class ConversationCreate(BaseModel):
    title:str


class ConversationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

class ConversationUpdate(BaseModel):
    title:str


class MessageResponse(BaseModel):
    id:int
    conversation_id:int
    role:str
    content:str

    model_config=ConfigDict(
        from_attributes=True
    )