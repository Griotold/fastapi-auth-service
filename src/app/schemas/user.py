from datetime import datetime

from pydantic import BaseModel, Field

class UserBase(BaseModel):
    email: str
    username: str

class UserCreate(UserBase):
    password: str = Field(..., min_length=8) # ✅ 이렇게 하면 필수 필드 (꼭 있어야 함)

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config: # SQLAlchemy ORM 모델을 Pydantic 모델로 변환할 수 있게 해주는 설정
        from_attributes = True