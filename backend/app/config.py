from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_DSN: str = "postgresql+psycopg://pao:pao@db:5432/pao"
    JWT_SECRET: str = "change-me"
    JWT_EXPIRE_MINUTES: int = 60
    JWT_REFRESH_EXPIRE_DAYS: int = 7
    TZ: str = "America/Sao_Paulo"
    CORS_ORIGINS: list[str] = ["*"]

    # SEED do admin padrão
    AUTO_SEED_ADMIN: bool = True
    DEFAULT_ADMIN_EMAIL: str = "pedepao"
    DEFAULT_ADMIN_PASSWORD: str = "pedepao"
    DEFAULT_ADMIN_FULLNAME: str = "Admin PedePao"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
