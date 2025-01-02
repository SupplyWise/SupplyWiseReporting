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
    """Returns a valid report creation for service tests."""
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
            items=[
                Item(id=uuid4(), name='Item A', barcode=1234567890, quantity=5.0),
                Item(id=uuid4(), name='Item B', barcode=1234567891, quantity=10.0),
            ]
        ),
        report_name="Monthly Inventory Report"
    )

def generate_valid_report_request_json() -> dict:
    """Returns a valid JSON-like dictionary for report creation in route tests."""
    return {
        "company_data": {
            "id": str(uuid4()),  # Convert UUID to string for JSON compatibility
            "name": "Test Company",
        },
        "restaurant_data": {
            "id": str(uuid4()),
            "name": "Test Restaurant",
        },
        "user_data": {
            "id": str(uuid4()),
            "name": "Test User",
        },
        "inventory_data": {
            "expected_close_time": (datetime.now() + timedelta(hours=1)).isoformat(),
            "actual_close_time": datetime.now().isoformat(),
            "items": [
                {"id": str(uuid4()), "name": 'Item A', "barcode": 1234567890, "quantity": 5.0},
                {"id": str(uuid4()), "name": 'Item B', "barcode": 1234567891, "quantity": 10.0},
            ],
        },
        "report_name": "Monthly Inventory Report",
    }