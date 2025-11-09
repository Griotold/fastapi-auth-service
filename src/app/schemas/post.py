from datetime import datetime
from pydantic import BaseModel

class PostCreate(BaseModel):
    title: str
    author: str
    content: str

class PostResponse(BaseModel):
    id: int
    title: str
    author: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True