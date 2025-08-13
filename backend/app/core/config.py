from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    api_name: str = "PedePao"
    api_base_path: str = "/api"
    database_url: str
    tz: str = "America/Sao_Paulo"
    cutoff_default: str = "13:00"

    model_config = SettingsConfigDict(env_prefix="PEDEPAO_", env_file=".env", extra="ignore")

settings = Settings()
