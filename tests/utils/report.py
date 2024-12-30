from uuid import uuid4
from datetime import datetime, timedelta

def generate_valid_report_request():
    """Retorna uma estrutura válida de ReportRequest"""
    return {
        "company_restaurant_data": {
            "company_id": str(uuid4()),
            "company_name": "Test Company",
            "restaurant_id": str(uuid4()),
            "restaurant_name": "Test Restaurant",
        },
        "user_data": {
            "user_id": str(uuid4()),
            "user_name": "Test User",
        },
        "inventory_expected_close_time": (datetime.now() + timedelta(hours=1)).isoformat(),
        "inventory_actual_close_time": datetime.now().isoformat(),
        "products": [
            {"id": str(uuid4()), "name": "Product A", "barcode": 1234567890, "quantity": 5.0},
            {"id": str(uuid4()), "name": "Product B", "barcode": 1234567891, "quantity": 10.0},
        ],
        "report_name": "End of Year Report",
    }