from pydantic import BaseSettings, Field


class APISettings(BaseSettings):
    SECRET_KEY = Field(default="your-secret-key-here")
    ALGORITHM = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = Field(default=30)
    EMAIL_CONFIRMATION_EXPIRE_HOURS = Field(default=24)


api_settings = APISettings()