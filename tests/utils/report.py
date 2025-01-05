from uuid import uuid4
from datetime import datetime, timedelta
from src.models.entities import (
    CompanyData,
    RestaurantData,
    UserData,
    InventoryData,
    Item,
    ItemCategory,
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
            starting_time=datetime.now() - timedelta(days=1),
            closure_time=datetime.now(),
            items=[
                Item(id=uuid4(), name='Coke', barcode=1234567890, quantity=5.0, category=ItemCategory.DRINKABLE),
                Item(id=uuid4(), name='Burger', barcode=1234567891, quantity=10.0, category=ItemCategory.EATABLE),
                Item(id=uuid4(), name='Fries', barcode=1234567892, quantity=8.0, category=ItemCategory.EATABLE),
                Item(id=uuid4(), name='Custom Item', barcode=1234567893, quantity=2.0, category=ItemCategory.CUSTOM),
                #* No unknow item to verify the category is not included in the report
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
            "starting_time": (datetime.now() - timedelta(days=1)).isoformat(),
            "closure_time": datetime.now().isoformat(),
            "items": [
                {"id": str(uuid4()), "name": 'Coke', "barcode": 1234567890, "quantity": 5.0, "category": "DRINKABLE"},
                {"id": str(uuid4()), "name": 'Burger', "barcode": 1234567891, "quantity": 10.0, "category": "EATABLE"},
                {"id": str(uuid4()), "name": 'Fries', "barcode": 1234567892, "quantity": 8.0, "category": "EATABLE"},
                {"id": str(uuid4()), "name": 'Custom Item', "barcode": 1234567893, "quantity": 2.0, "category": "CUSTOM"},
                #* No unknow item to verify the category is not included in the report
            ]
        },
        "report_name": "Monthly Inventory Report",
    }