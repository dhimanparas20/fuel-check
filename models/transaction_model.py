import time
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

class TransactionBase(BaseModel):
    id: Optional[str] = None  # MongoDB ObjectId as string
    vehicle_id: str = Field(...)
    amount: int = Field(..., ge=0, le=1000000)
    fuel_quantity: int = Field(..., ge=0, le=1000000)
    location: str = Field(..., min_length=3, max_length=50)
    tank_fully_filled: bool = Field(...)
    created_at: float = Field(default_factory=lambda: time.time())
    updated_at: float = Field(default_factory=lambda: time.time())

class CreateTransaction(TransactionBase):
    pass

class ReadTransaction(TransactionBase):
    pass

class UpdateTransaction(TransactionBase):
    vehicle_id: Optional[str] = None
    amount: Optional[int] = None
    fuel_quantity: Optional[int] = None
    location: Optional[str] = None
    tank_fully_filled: Optional[bool] = None
    created_at: Optional[float] = None
    updated_at: Optional[float] = None

class DeleteTransaction(TransactionBase):
    id: str

