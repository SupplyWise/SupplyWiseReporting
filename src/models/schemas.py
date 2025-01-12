from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from typing import List, Optional

# Get the entities that constitute the report data
from .entities import CompanyData, RestaurantData, UserData, InventoryData

# Requirements to create a report
#*Note: No response schema for report creation as it streams the file directly.
class ReportCreateRequest(BaseModel):
    company_data: CompanyData
    restaurant_data: RestaurantData
    user_data: UserData
    inventory_data: InventoryData
    report_name: Optional[str] = Field(default=None, description="Optional custom name for the report")
    
    @model_validator(mode='after')
    def check_valid_report_name(cls, values):
        report_name = values.report_name
        if report_name and not 3 <= len(report_name) <= 100:
            raise ValueError('Report Name must be between 3 and 100 characters long')
        return values

# What can be shown in each report in the user interface
class ReportMetadata(BaseModel):
    report_id: str = Field(..., description="Unique identifier for the report")
    report_name: str = Field(..., description="Name of the report")
    created_at: datetime = Field(..., description="Timestamp when the report was created")
    user_name: str = Field(..., description="Name of the user who generated the report")

# Paginated response for listing reports in a certain restaurant
class PaginatedReportsResponse(BaseModel):
    reports: List[ReportMetadata] = Field(..., description="List of reports for the restaurant")
    total: int = Field(..., description="Total number of reports available")
    page: int = Field(..., description="Current page number")
    per_page: int = Field(..., description="Number of reports per page")
