from src.services.report_generator import ReportGenerator
from src.models.schemas import ReportRequest
from uuid import uuid4
from datetime import datetime

def test_generate_report_success():
    generator = ReportGenerator()
    report_request = ReportRequest(
        company_restaurant_data={
            "company_id": uuid4(),
            "company_name": "Test Company",
            "restaurant_id": uuid4(),
            "restaurant_name": "Test Restaurant",
        },
        user_data={
            "user_id": uuid4(),
            "user_name": "Test User",
        },
        inventory_expected_close_time=datetime.now(),
        inventory_actual_close_time=datetime.now(),
        products=[
            {"id": uuid4(), "name": "Product A", "barcode": 1234567890, "quantity": 5.0},
            {"id": uuid4(), "name": "Product B", "barcode": 1234567891, "quantity": 10.0},
        ],
        report_name="Monthly Inventory Report",
    )

    pdf_content = generator.generate_report(report_request)
    assert isinstance(pdf_content, bytes)
    assert len(pdf_content) > 0

def test_generate_report_with_many_products():
    generator = ReportGenerator()
    products = [
        {"id": uuid4(), "name": f"Product {i}", "barcode": 1000 + i, "quantity": i * 1.0}
        for i in range(1, 101)
    ]
    report_request = ReportRequest(
        company_restaurant_data={
            "company_id": uuid4(),
            "company_name": "Test Company",
            "restaurant_id": uuid4(),
            "restaurant_name": "Test Restaurant",
        },
        user_data={
            "user_id": uuid4(),
            "user_name": "Test User",
        },
        inventory_expected_close_time=datetime.now(),
        inventory_actual_close_time=datetime.now(),
        products=products,
        report_name="Massive Inventory Report",
    )
    pdf_content = generator.generate_report(report_request)
    assert isinstance(pdf_content, bytes)
    assert len(pdf_content) > 0
