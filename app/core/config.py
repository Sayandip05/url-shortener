from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    app_name: str = "URL Shortener"
    base_url: str = "http://localhost:8000"
    database_url: str = "sqlite:///./urls.db"


settings = Settings()
