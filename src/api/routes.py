from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse, FileResponse, RedirectResponse

from src.models.schemas import (
    ReportCreateRequest, 
    ReportMetadata,
    PaginatedReportsResponse, 
)
from src.services.report_generator import ReportGenerator
from src.services.storage import StorageService, LocalStorageService, S3StorageService
from src.core.config import get_settings, StorageType
from uuid import uuid4

import logging

logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/reports")


def get_storage_service() -> StorageService:
    settings = get_settings()
    if settings.storage_type == StorageType.LOCAL:
        logging.info("Using LocalStorageService")
        return LocalStorageService()
    logging.info("Using S3StorageService")
    return S3StorageService()


@router.post("/", response_model=None)
async def generate_report(
    report_data: ReportCreateRequest,
    storage_service=Depends(get_storage_service),
):
    """
    Generates a PDF report and streams it back to the client.
    """
    try:
        logging.info("Initializing report generation...")
        
        # Generate a unique report ID
        closing_time = report_data.inventory_data.actual_close_time.strftime('%Y-%m-%d')
        unique_suffix = str(uuid4()) # Add a unique suffix to avoid ID conflicts
        report_id = f"{report_data.company_data.id}-{report_data.restaurant_data.id}-{closing_time}-{unique_suffix}"
        
        # Generate PDF
        generator = ReportGenerator()
        pdf_content = generator.generate_report(report_data)
        
        # Save the PDF
        logging.info(f"Saving report {report_id}...")
        storage_path = await storage_service.save_report(report_id, pdf_content)
        
        # Stream the PDF to the client
        pdf_file = open(storage_path, "rb")
        return StreamingResponse(pdf_file, media_type="application/pdf", headers={
            "Content-Disposition": f"attachment; filename={report_id}.pdf"
        })
    except Exception as e:
        logging.error(f"Error generating report: {e}")
        raise HTTPException(status_code=500, detail="Internal error generating the report.")


@router.get("/", response_model=PaginatedReportsResponse)
async def list_reports(
    company_id: str,
    restaurant_id: str,
    page: int = Query(1, ge=1),
    per_page: int = Query(12, ge=1, le=48),
    storage_service=Depends(get_storage_service),
):
    """
    Lists metadata for reports, paginated.
    """
    logging.info(f"Listing reports for company ID {company_id} and restaurant ID {restaurant_id}...")
    
    try:
        # Fetch reports
        result = await storage_service.list_reports_by_restaurant(company_id, restaurant_id, page, per_page)
    except ValueError as e:
        # Handle errors
        error_message = str(e)
        if "No reports found" in error_message:
            logging.warning("No reports found.")
            raise HTTPException(status_code=404, detail="No reports found.")
        elif "out of range" in error_message:
            logging.error(f"Invalid page requested: {error_message}")
            raise HTTPException(status_code=400, detail=error_message)
        
    # Return paginated response
    logging.info(f"Returning {len(result.reports)} reports for company ID {company_id} and restaurant ID {restaurant_id}.")
    return result


@router.get("/{report_id}", response_model=None)
async def download_report(
    report_id: str,
    storage_service=Depends(get_storage_service),
):
    """
    Downloads a specific report by ID.
    """
    logging.info(f"Downloading report: {report_id}")
    try:
        # Obtain local path or S3 URL
        logging.info("Getting report path or S3 URL...")
        report_path = await storage_service.get_report_path(report_id)
        if isinstance(storage_service, LocalStorageService):
            logging.info("Returning file response...")
            return FileResponse(report_path, media_type="application/pdf", filename=f"{report_id}.pdf")
        else:
            logging.info("Returning redirect response...")
            return RedirectResponse(report_path)  # Return URL for S3
    except FileNotFoundError:
        logging.error(f"Report {report_id} not found.")
        raise HTTPException(status_code=404, detail=f"Report with ID {report_id} not found.")
