from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = 'CPP Atlas API'
    environment: str = 'development'
    database_url: str = 'postgresql+psycopg://cppatlas:cppatlas@postgres:5432/cppatlas'
    jwt_secret: str = 'development-only-change-this-secret'
    jwt_exp_minutes: int = 60
    cors_origins: str = 'http://localhost:4173,http://localhost:8080'
    llm_base_url: str | None = None
    llm_api_key: str | None = None
    llm_model: str | None = None
    llm_timeout: int = 30
    runner_url: str = 'http://runner:8010'
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(',') if origin.strip()]

@lru_cache
def get_settings() -> Settings:
    return Settings()
