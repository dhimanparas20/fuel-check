from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from modules.utils import get_timestamp


class VehicleBase(BaseModel):
    id: Optional[str] = None  # MongoDB ObjectId as string
    owner_id: str = Field(...)
    name: str = Field(..., min_length=3, max_length=50)
    model: str = Field(..., min_length=3, max_length=50)
    color: str = Field(..., min_length=3, max_length=50)
    company: str = Field(..., min_length=3, max_length=50)
    current_mileage: int = Field(..., ge=0, le=1000000)
    registration_number: str = Field(..., min_length=3, max_length=50)
    total_kms_driven: int = Field(..., ge=0, le=1000000)
    created_at: float = Field(default_factory=lambda: get_timestamp())
    updated_at: float = Field(default_factory=lambda: get_timestamp())
    fuel_type: Optional[str] = None
    last_service_date: Optional[str] = None
    average_mileage: Optional[int] = None
    chasis_number: Optional[str] = None
    fuel_tank_capacity: Optional[int] = None

class CreateVehicle(VehicleBase):
    pass

class ReadVehicle(VehicleBase):
    pass

class UpdateVehicle(VehicleBase):
    name: Optional[str] = None
    model: Optional[str] = None
    color: Optional[str] = None
    company: Optional[str] = None
    current_mileage: Optional[int] = None
    registration_number: Optional[str] = None
    total_kms_driven: Optional[int] = None
    created_at: Optional[float] = None
    updated_at: float = Field(default_factory=lambda: get_timestamp())
    last_service_date: Optional[str] = None
    average_mileage: Optional[int] = None
    chasis_number: Optional[str] = None
    fuel_tank_capacity: Optional[int] = None
    fuel_type: Optional[str] = None

class DeleteVehicle(VehicleBase):
    id: str