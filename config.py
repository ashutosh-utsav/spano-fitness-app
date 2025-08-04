from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    GEMINI_API_KEY: str

    DEFAULT_USER_USERNAME: str
    DEFAULT_USER_PASSWORD: str
    DEFAULT_ADMIN_USERNAME: str
    DEFAULT_ADMIN_PASSWORD: str

    class Config:
        env_file = ".env"

settings = Settings()
