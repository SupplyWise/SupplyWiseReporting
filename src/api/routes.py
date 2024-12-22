from fastapi import APIRouter, Depends, HTTPException
from src.models.schemas import ReportRequest, ReportResponse
from src.services.report_generator import ReportGenerator
from src.services.storage import LocalStorageService, S3StorageService
from src.core.config import get_settings, StorageType
from datetime import datetime
import logging

# Configure the logger
logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/reports")

# Obtain the storage service based on the configuration
def get_storage_service():
    settings = get_settings()
    if settings.storage_type == StorageType.LOCAL:
        print("Using LocalStorageService")
        return LocalStorageService()
    print("Using S3StorageService")
    return S3StorageService()

@router.post("/", response_model=ReportResponse)
async def generate_report(
    report_data: ReportRequest,
    storage_service=Depends(get_storage_service),
):
    """
    Generates a PDF report and saves it to the storage service.
    """
    try:
        logging.info("Initializing report generation...")
        
        # Generate a unique report ID
        report_id = f"{datetime.now().strftime('%Y-%m-%d')}-{report_data.company_id}-{report_data.restaurant_id}"
        
        # Generate a PDF
        generator = ReportGenerator()
        pdf_content = generator.generate_report(report_data)
        
        # Save the PDF
        storage_path = await storage_service.save_report(report_id, pdf_content)
        
        logging.info(f"Report {report_id} successfully generated.")
        return ReportResponse(
            report_id=report_id,
            created_at=datetime.now(),
            storage_path=storage_path,
        )

    except Exception as e:
        logging.error(f"Error generating report: {e}")
        raise HTTPException(status_code=500, detail="Internal error generating the report.")

@router.get("/{report_id}")
async def get_report(
    report_id: str,
    storage_service=Depends(get_storage_service),
):
    """
    Retrieves a previously generated report.
    """
    try:
        logging.info(f"Retrieving report: {report_id}")
        return await storage_service.get_report(report_id)
    except FileNotFoundError:
        logging.warning(f"Report with ID {report_id} was not found.")
        raise HTTPException(status_code=404, detail="Report not found.")
