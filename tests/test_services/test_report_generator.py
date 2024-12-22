import pytest
from src.services.report_generator import ReportGenerator
from src.models.schemas import ReportRequest, ProductQuantity
from uuid import uuid4
from datetime import datetime

def test_generate_report_success():
    generator = ReportGenerator()
    report_request = ReportRequest(
        company_id=uuid4(),
        company_name="Test Company",
        restaurant_id=uuid4(),
        restaurant_name="Test Restaurant",
        user_id=uuid4(),
        user_name="Test User",
        inventory_close_time=datetime.now(),
        products=[
            ProductQuantity(product_id=uuid4(), product_name="Product A", quantity=5.0),
            ProductQuantity(product_id=uuid4(), product_name="Product B", quantity=10.0),
        ],
    )

    pdf_content = generator.generate_report(report_request)
    assert isinstance(pdf_content, bytes)
    assert len(pdf_content) > 0
