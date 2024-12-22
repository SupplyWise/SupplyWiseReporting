from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime
from typing import List
from uuid import UUID

class ProductQuantity(BaseModel):
    product_id: UUID
    product_name: str
    quantity: float

    @field_validator('quantity')
    def quantity_non_negative(cls, v):
        if v < 0:
            raise ValueError('Product Quantity must be non-negative')
        return v

class ReportRequest(BaseModel):
    company_id: UUID
    company_name: str
    restaurant_id: UUID
    restaurant_name: str
    user_id: UUID
    user_name: str
    inventory_close_time: datetime
    products: List[ProductQuantity]

    @model_validator(mode='after')
    def check_products_non_empty(cls, values):
        products = values.products
        if not products:
            raise ValueError('Products list must not be empty')
        return values

class ReportResponse(BaseModel):
    report_id: str = Field(..., example="2024-03-22-company1-restaurant2")
    created_at: datetime
    storage_path: str