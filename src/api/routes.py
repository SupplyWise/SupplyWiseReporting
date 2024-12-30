from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse

from src.models.schemas import (
    ReportCreateRequest, 
    PaginatedReportsResponse, 
)
from src.services.report_generator import ReportGenerator
from src.services.storage import StorageService, LocalStorageService, S3StorageService
from src.core.config import get_settings, StorageType

from datetime import datetime
import logging
import os

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
        report_id = f"{closing_time}-{report_data.company_data.id}-{report_data.restaurant_data.id}"
        
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
    try:
        reports, total = await storage_service.list_reports_by_restaurant(company_id, restaurant_id, page, per_page)
        if not reports:
            raise HTTPException(status_code=404, detail="No reports found.")
        
        return PaginatedReportsResponse(
            reports=reports,
            total=total,
            page=page,
            per_page=per_page,
        )
    except Exception as e:
        logging.error(f"Error listing reports: {e}")
        raise HTTPException(status_code=500, detail="Internal error listing reports.")


@router.get("/{report_id}", response_model=None)
async def download_report(
    report_id: str,
    storage_service=Depends(get_storage_service),
):
    """
    Downloads a specific report by ID.
    """
    try:
        logging.info(f"Downloading report: {report_id}")
        file_path = await storage_service.get_report_path(report_id)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Report not found.")
        
        pdf_file = open(file_path, "rb")
        return StreamingResponse(pdf_file, media_type="application/pdf", headers={
            "Content-Disposition": f"attachment; filename={report_id}.pdf"
        })
    except Exception as e:
        logging.error(f"Error downloading report {report_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal error downloading the report.")
