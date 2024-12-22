import os
import boto3

class LocalStorageService:
    def __init__(self, base_dir="./reports"):
        os.makedirs(base_dir, exist_ok=True)
        self.base_dir = base_dir

    async def save_report(self, report_id: str, content: bytes) -> str:
        file_path = os.path.join(self.base_dir, f"{report_id}.pdf")
        with open(file_path, "wb") as f:
            f.write(content)
        return file_path

    async def get_report(self, report_id: str) -> bytes:
        file_path = os.path.join(self.base_dir, f"{report_id}.pdf")
        if not os.path.exists(file_path):
            raise FileNotFoundError
        with open(file_path, "rb") as f:
            return f.read()

class S3StorageService:
    def __init__(self):
        self.s3 = boto3.client("s3")
        self.bucket_name = "mock-s3-bucket" #TODO: Change this to the S3 bucket name

    async def save_report(self, report_id: str, content: bytes) -> str:
        self.s3.put_object(Bucket=self.bucket_name, Key=f"{report_id}.pdf", Body=content)
        return f"s3://{self.bucket_name}/{report_id}.pdf"

    async def get_report(self, report_id: str) -> bytes:
        obj = self.s3.get_object(Bucket=self.bucket_name, Key=f"{report_id}.pdf")
        return obj["Body"].read()
