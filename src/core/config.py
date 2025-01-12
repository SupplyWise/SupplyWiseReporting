from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from enum import Enum

class StorageType(str, Enum):
    LOCAL = "LOCAL"
    S3 = "S3"

class Settings(BaseSettings):
    # General settings
    app_name: str = "Reports Service"
    debug: bool = True

    #TODO: temporary locally only
    storage_type: StorageType = StorageType.LOCAL

    # # Storage settings
    # storage_type: str = Field("LOCAL", env="STORAGE_TYPE")  # LOCAL or S3
    # s3_bucket_name: str = Field(None, env="S3_BUCKET_NAME")

    # # AWS settings (if needed)
    # aws_access_key: str = Field(None, env="AWS_ACCESS_KEY")
    # aws_secret_key: str = Field(None, env="AWS_SECRET_KEY")
    # aws_region: str = Field(None, env="AWS_REGION")

    # ConfigDict to load environment variables (Class Config is deprecated)
    model_config = ConfigDict(env_file=".env")

# Method to retrieve the settings
def get_settings() -> Settings:
    return Settings()
