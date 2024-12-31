from uuid import uuid4
from datetime import datetime, timedelta
from src.models.entities import (
    CompanyData,
    RestaurantData,
    UserData,
    InventoryData,
    Item,
)
from src.models.schemas import ReportCreateRequest

def generate_valid_report_request() -> ReportCreateRequest:
    """Returns a valid request for report creation in tests."""
    return ReportCreateRequest(
        company_data=CompanyData(
            id=uuid4(),
            name="Test Company"
        ),
        restaurant_data=RestaurantData(
            id=uuid4(),
            name="Test Restaurant"
        ),
        user_data=UserData(
            id=uuid4(),
            name="Test User"
        ),
        inventory_data=InventoryData(
            expected_close_time=datetime.now() + timedelta(hours=1),
            actual_close_time=datetime.now(),
            products=[
                Item(id=uuid4(), name="Product A", barcode=1234567890, quantity=5.0),
                Item(id=uuid4(), name="Product B", barcode=1234567891, quantity=10.0),
            ]
        ),
        report_name="Monthly Inventory Report"
    )