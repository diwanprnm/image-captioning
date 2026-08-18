from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings loaded from .env file."""

    PROJECT_NAME: str = "Image Captioning Service"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    #9Router
    NINE_ROUTER_BASE_URL: str="http://103.59.160.103:20128/v1"
    NINE_ROUTER_API_KEY: str= "sk-1fba0bbe79a12d5b-elc2mq-d3dc2dfa"
    NINE_ROUTER_VISION_MODEL : str = "combofreetwo"

    
    # Database (Postgres)
    POSTGRES_SERVER: str = "db"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "caption_db"
    POSTGRES_PORT: int = 5433
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()