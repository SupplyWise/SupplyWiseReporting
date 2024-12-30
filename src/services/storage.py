import os
import boto3
from datetime import datetime

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

    async def list_reports_by_restaurant(self, company_id: str, restaurant_id: str) -> List[Dict]:
        """
        Lists all report files with metadata for a specific company and restaurant.
        """
        report_files = []
        prefix = f"{company_id}-{restaurant_id}-"
        for file_name in os.listdir(self.base_dir):
            if file_name.startswith(prefix) and file_name.endswith(".pdf"):
                file_path = os.path.join(self.base_dir, file_name)
                created_at = datetime.fromtimestamp(os.path.getctime(file_path))
                report_files.append({"file_name": file_name, "created_at": created_at})
        return report_files

    async def get_report(self, report_id: str) -> bytes:
        """
        Retrieves a report file from the local filesystem.
        """
        file_path = os.path.join(self.base_dir, f"{report_id}.pdf")
        if not os.path.exists(file_path):
            raise FileNotFoundError
        with open(file_path, "rb") as f:
            return f.read()

class S3StorageService(StorageService):
    def __init__(self):
        self.s3 = boto3.client("s3")
        self.bucket_name = "mock-s3-bucket" #TODO: Change this to the S3 bucket name

    async def save_report(self, report_id: str, content: bytes) -> str:
        self.s3.put_object(Bucket=self.bucket_name, Key=f"{report_id}.pdf", Body=content)
        return f"s3://{self.bucket_name}/{report_id}.pdf"
    
    async def list_reports_by_restaurant(self, company_id: str, restaurant_id: str, max_results=10, continuation_token=None) -> dict:
        """
        Lists all reports for a specific company and restaurant from S3 with pagination.
        """
        prefix = f"{company_id}-{restaurant_id}-"
        params = {
            "Bucket": self.bucket_name,
            "Prefix": prefix,
            "MaxKeys": max_results
        }
        if continuation_token:
            params["ContinuationToken"] = continuation_token

        response = self.s3.list_objects_v2(**params)
        reports = []
        for obj in response.get("Contents", []):
            reports.append({
                "file_name": obj["Key"],
                "last_modified": obj["LastModified"]
            })
        
        return {
            "reports": reports,
            "next_token": response.get("NextContinuationToken")
        }

    async def get_report(self, report_id: str) -> bytes:
        obj = self.s3.get_object(Bucket=self.bucket_name, Key=f"{report_id}.pdf")
        return obj["Body"].read()
