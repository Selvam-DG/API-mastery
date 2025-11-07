from pydantic import BaseModel, Field
from typing import Literal

class WSInMessage(BaseModel):
    type: Literal["chat"] = Field(default="chat")
    text: str = Field(min_length=1, max_length=2000)
    

class WSOutMessage(BaseModel):
    type: Literal["chat", "system"] = "chat"
    sender: str
    text: str
    room: str