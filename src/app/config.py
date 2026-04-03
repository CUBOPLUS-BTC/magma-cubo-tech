from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./satsscore.db"
    JWT_SECRET: str = "dev-secret-change-in-prod"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 30
    MEMPOOL_API_URL: str = "https://mempool.space/api"
    COINGECKO_API_KEY: str = ""
    CORS_ORIGINS: list[str] = [
        "http://localhost:8080",
    ]

    class Config:
        env_file = ".env"


settings = Settings()
