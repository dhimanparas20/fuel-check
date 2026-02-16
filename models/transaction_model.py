from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from modules.utils import get_timestamp


class TransactionBase(BaseModel):
    id: Optional[str] = None  # MongoDB ObjectId as string
    vehicle_id: str = Field(...)
    amount: int = Field(..., ge=0, le=1000000)
    fuel_quantity: int = Field(..., ge=0, le=1000000)
    location: str = Field(..., min_length=3, max_length=50)
    tank_fully_filled: bool = Field(...)
    created_at: float = Field(default_factory=lambda: get_timestamp())
    updated_at: float = Field(default_factory=lambda: get_timestamp())

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
    updated_at: float = Field(default_factory=lambda: get_timestamp())

class DeleteTransaction(TransactionBase):
    id: str

