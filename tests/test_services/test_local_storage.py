import os
import pytest
from uuid import uuid4
from src.services.storage import LocalStorageService

@pytest.fixture
def storage_service():
    return LocalStorageService()

@pytest.mark.asyncio
async def test_save_and_get_report(storage_service):
    report_id = f"test-report-{uuid4()}"
    pdf_content = b"Fake PDF content"
    
    # Test saving the report
    path = await storage_service.save_report(report_id, pdf_content)
    assert os.path.exists(path)

    # Test retrieving the report
    retrieved_pdf = await storage_service.get_report(report_id)
    assert retrieved_pdf == pdf_content

    # Cleanup
    os.remove(path)

@pytest.mark.asyncio
async def test_get_report_not_found(storage_service):
    with pytest.raises(FileNotFoundError):
        await storage_service.get_report("non-existent-report")
