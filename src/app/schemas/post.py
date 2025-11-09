from datetime import datetime
from pydantic import BaseModel

class PostCreate(BaseModel):
    title: str
    author: str
    content: str

class PostUpdate(BaseModel):
    title: str | None = None    # str 또는 None 가능, 기본값은 None
    content: str | None = None

class PostResponse(BaseModel):
    id: int
    title: str
    author: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

