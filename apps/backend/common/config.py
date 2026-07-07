from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+asyncpg://chess:chess@localhost:5432/chess"
    cors_origins: list[str] = ["http://localhost:3000"]


settings = Settings()
