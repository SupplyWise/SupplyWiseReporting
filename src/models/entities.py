from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime
from typing import List
from uuid import UUID
from enum import Enum

class CompanyData(BaseModel):
    id: UUID = Field(default_factory=UUID, description="Company ID")
    name: str = Field(..., description="Company name")

class RestaurantData(BaseModel):
    id: UUID = Field(default_factory=UUID, description="Restaurant ID")
    name: str = Field(..., description="Restaurant name")

class UserData(BaseModel):
    id: UUID = Field(default_factory=UUID, description="User ID")
    name: str = Field(..., description="User name")

class ItemCategory(str, Enum):
    DRINKABLE = "DRINKABLE"
    EATABLE = "EATABLE"
    CUSTOM = "CUSTOM"
    UNKNOWN = "UNKNOWN" # This is a default value for the enum

class Item(BaseModel):
    id: UUID = Field(default_factory=UUID, description="Item ID")
    name: str = Field(..., min_length=3, max_length=100, description="Item name")
    barcode: int = Field(..., ge=0, description="Item barcode")
    quantity: float = Field(..., ge=0, description="Item quantity in stock (greater than or equal to 0)")
    category: ItemCategory = Field(..., description="Item category (drinkable, edible, custom, unknown)")

    @field_validator('barcode')
    def validate_barcode(cls, v):
        if not isinstance(v, int):
            raise ValueError('Barcode must be an integer')
        # Keep a diferent variable because pydantic will convert it to a string and ruin every report generation
        digit_count = len(str(v)) 
        if not 3 <= digit_count <= 30:
            raise ValueError('Barcode must be between 3 and 30 digits long')
        return v

class InventoryData(BaseModel):
    starting_time: datetime = Field(..., description="Strating timestamp of the inventory")
    closure_time: datetime = Field(..., description="Closing timestamp of the inventory")
    items: List[Item] = Field(..., description="List of items upon closure for the report", min_length=1)

    @model_validator(mode="after")
    def validate_time_order(self):
        if self.closure_time <= self.starting_time:
            raise ValueError('The closure time must be after the starting time')
        return self