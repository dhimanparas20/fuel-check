import time
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    id: Optional[str] = None  # MongoDB ObjectId as string
    full_name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(..., min_length=3, max_length=50)
    is_active: bool = True
    created_at: float = Field(default_factory=lambda: time.time())
    updated_at: float = Field(default_factory=lambda: time.time())

class CreateUser(BaseModel):
    pass

class ReadUser(UserBase):
    pass

class UpdateUser(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length=50)
    is_active: Optional[bool] = None
    updated_at: float = Field(default_factory=lambda: time.time())

class DeleteUser(BaseModel):
    id: str


class LoginUser(BaseModel):
    email: EmailStr = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=50)
