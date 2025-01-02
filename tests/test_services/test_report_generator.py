from uuid import uuid4
from tests.utils.report import generate_valid_report_request
from src.models.entities import Item
from src.services.report_generator import ReportGenerator

def test_generate_report_success():
    generator = ReportGenerator()
    report_request = generate_valid_report_request()

    pdf_content = generator.generate_report(report_request)
    assert isinstance(pdf_content, bytes)
    assert len(pdf_content) > 0


def test_generate_report_with_many_items():
    generator = ReportGenerator()
    report_request = generate_valid_report_request()
    report_request.inventory_data.items = [
        Item(id=uuid4(), name=f'Item {i}', barcode=1000 + i, quantity=i * 1.0)
        for i in range(1, 101)
    ]

    pdf_content = generator.generate_report(report_request)
    assert isinstance(pdf_content, bytes)
    assert len(pdf_content) > 0
