import time
from typing import Optional, List

from pydantic import BaseModel, EmailStr, Field
from uuid import UUID


class UserBase(BaseModel):
    id: Optional[str] = None  # MongoDB ObjectId as string
    full_name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(..., min_length=3, max_length=50)
    is_active: bool = True
    vehicles: List[UUID] = []
    created_at: float = Field(default_factory=lambda: time.time())
    updated_at: float = Field(default_factory=lambda: time.time())

class CreateUser(BaseModel):
    full_name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=50)
    vehicles: List[UUID] = []
    is_active: bool = True
    created_at: float = Field(default_factory=lambda: time.time())
    updated_at: float = Field(default_factory=lambda: time.time())

class ReadUser(UserBase):
    pass

class UpdateUser(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length=50)
    vehicles: Optional[List[UUID]] = None
    is_active: Optional[bool] = None
    updated_at: float = Field(default_factory=lambda: time.time())

class DeleteUser(BaseModel):
    id: str
    email: Optional[EmailStr] = None


class LoginUser(BaseModel):
    email: EmailStr = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=50)
