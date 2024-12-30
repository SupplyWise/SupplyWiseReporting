from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import List
from uuid import UUID

class CompanyData(BaseModel):
    id: UUID = Field(default_factory=UUID, description="Company ID")
    name: str = Field(..., description="Company name")

class RestaurantData(BaseModel):
    id: UUID = Field(default_factory=UUID, description="Restaurant ID")
    name: str = Field(..., description="Restaurant name")

class UserData(BaseModel):
    id: UUID = Field(default_factory=UUID, description="User ID")
    name: str = Field(..., description="User name")

class Item(BaseModel):
    id: UUID = Field(default_factory=UUID, description="Product ID")
    name: str = Field(..., description="Product name")
    barcode: int = Field(..., description="Product barcode")
    quantity: float = Field(..., ge=0, description="Product quantity in stock (greater than or equal to 0)")

    @field_validator('name')
    def name_length(cls, v):
        if not 3 <= len(v) <= 100:
            raise ValueError('Item Name must be between 3 and 100 characters long')

    @field_validator('barcode')
    def barcode_length(cls, v):
        if not 3 <= len(str(v)) <= 30:
            raise ValueError('Item Barcode must be between 3 and 30 digits long')

class InventoryData(BaseModel):
    expected_close_time: datetime = Field(..., description="Expected close time of the inventory")
    actual_close_time: datetime = Field(..., description="Actual close time of the inventory")
    products: List[Item] = Field(..., description="List of products for the report", min_length=1)