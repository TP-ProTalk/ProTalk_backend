from pydantic import Field
from pydantic_settings import BaseSettings


class APISettings(BaseSettings):
    SECRET_KEY: str = Field(default="your-secret-key-here")
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    EMAIL_CONFIRMATION_EXPIRE_HOURS: int = Field(default=24)

    # Настройки SMTP для отправки email
    SMTP_HOST: str = Field(default="smtp.example.com")
    SMTP_PORT: int = Field(default=587)
    SMTP_USER: str = Field(default="user@example.com")
    SMTP_PASSWORD: str = Field(default="hashed_password")
    SMTP_FROM: str = Field(default="noreply@example.com")

    # Базовый URL API
    API_BASE_URL: str = Field(default="http://localhost:8000")

    class Config:
        env_file = ".env"
        case_sensitive = True


api_settings = APISettings()