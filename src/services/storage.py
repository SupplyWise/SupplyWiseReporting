import os
import boto3
from datetime import datetime
from math import ceil

from abc import ABC, abstractmethod
from typing import List, Dict

class StorageService(ABC):
    @abstractmethod
    async def save_report(self, report_id: str, content: bytes) -> str:
        """
        Save a report file and return the storage path.
        """
        pass

    @abstractmethod
    async def list_reports_by_restaurant(self, company_id: str, restaurant_id: str) -> List[Dict]:
        """
        List all reports for a specific company and restaurant with metadata.
        """
        pass

    @abstractmethod
    async def get_report(self, report_id: str) -> bytes:
        """
        Retrieve a report file by its ID.
        """
        pass

class LocalStorageService(StorageService):
    def __init__(self, base_dir="./reports"):
        os.makedirs(base_dir, exist_ok=True)
        self.base_dir = base_dir

    async def save_report(self, report_id: str, content: bytes) -> str:
        """
        Saves a report file to the local filesystem.
        """
        file_path = os.path.join(self.base_dir, f"{report_id}.pdf")
        with open(file_path, "wb") as f:
            f.write(content)
        return file_path

#TODO maybe remove pagination and list all instead
    # async def list_reports_by_restaurant(self, company_id: str, restaurant_id: str) -> List[Dict]:
    #     """
    #     Lists all report files with metadata for a specific company and restaurant.
    #     """
    #     report_files = []
    #     prefix = f"{company_id}-{restaurant_id}-"
    #     for file_name in os.listdir(self.base_dir):
    #         if file_name.startswith(prefix) and file_name.endswith(".pdf"):
    #             file_path = os.path.join(self.base_dir, file_name)
    #             created_at = datetime.fromtimestamp(os.path.getctime(file_path))
    #             report_files.append({"file_name": file_name, "created_at": created_at})
    #     return report_files

    async def list_reports_by_restaurant(self, company_id: str, restaurant_id: str, page: int, per_page: int) -> Dict:
        """
        Lists report files with metadata for a specific company and restaurant with pagination.
        """
        report_files = []
        prefix = f"{company_id}-{restaurant_id}-"
        
        # Filter by prefix
        for file_name in os.listdir(self.base_dir):
            if file_name.startswith(prefix) and file_name.endswith(".pdf"):
                file_path = os.path.join(self.base_dir, file_name)
                created_at = datetime.fromtimestamp(os.path.getctime(file_path))
                report_files.append({"file_name": file_name, "created_at": created_at})
        
        # Order by latest created
        report_files.sort(key=lambda x: x["created_at"], reverse=True)
        
        # Pagination logic
        total_reports = len(report_files)
        total_pages = ceil(total_reports / per_page)
        start = (page - 1) * per_page
        end = start + per_page
        paginated_reports = report_files[start:end]

        return {
            "reports": paginated_reports,
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages,
            "total_reports": total_reports,
        }

    async def get_report(self, report_id: str) -> bytes:
        """
        Retrieves a report file from the local filesystem.
        """
        file_path = os.path.join(self.base_dir, f"{report_id}.pdf")
        if not os.path.exists(file_path):
            raise FileNotFoundError
        with open(file_path, "rb") as f:
            return f.read()
        
    async def get_report_path(self, report_id: str) -> str:
        """
        Retuns a report file path from the local filesystem.
        """
        file_path = os.path.join(self.base_dir, f"{report_id}.pdf")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Report {report_id} not found.")
        return file_path

class S3StorageService(StorageService):
    def __init__(self):
        self.s3 = boto3.client("s3")
        self.bucket_name = "mock-s3-bucket" #TODO: Change this to the S3 bucket name

    async def save_report(self, report_id: str, content: bytes) -> str:
        self.s3.put_object(Bucket=self.bucket_name, Key=f"{report_id}.pdf", Body=content)
        return f"s3://{self.bucket_name}/{report_id}.pdf"

    async def list_reports_by_restaurant(self, company_id: str, restaurant_id: str, page: int, per_page: int) -> Dict:
        """
        Lists reports for a specific company and restaurant from S3 with pagination.
        """
        # Use o cálculo de paginação para ajustar MaxKeys e ContinuationToken
        prefix = f"{company_id}-{restaurant_id}-"
        params = {
            "Bucket": self.bucket_name,
            "Prefix": prefix,
            "MaxKeys": per_page
        }
        if page > 1:
            params["ContinuationToken"] = self._get_continuation_token(page, per_page, prefix)
        
        response = self.s3.list_objects_v2(**params)
        reports = [
            {"file_name": obj["Key"], "last_modified": obj["LastModified"]}
            for obj in response.get("Contents", [])
        ]
        return {
            "reports": reports,
            "page": page,
            "per_page": per_page,
            "total_reports": response.get("KeyCount", 0),
            "next_token": response.get("NextContinuationToken"),
        }

    async def get_report(self, report_id: str) -> bytes:
        obj = self.s3.get_object(Bucket=self.bucket_name, Key=f"{report_id}.pdf")
        return obj["Body"].read()
    
    async def get_report_path(self, report_id: str) -> str:
        """
        Generates a pre-signed URL to download a report from S3.
        """
        return self.s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': self.bucket_name, 'Key': f"{report_id}.pdf"},
            ExpiresIn=3600  # URL valid for 1 hour
        )

