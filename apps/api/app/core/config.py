from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool

    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str

    DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    MEDIA_STORAGE_TYPE: str
    MEDIA_STORAGE_PATH: str
    MEDIA_BASE_URL: str

    # ------------------------------------------
    # Gemini AI
    # ------------------------------------------

    GEMINI_API_KEY: str

    GEMINI_EMBEDDING_MODEL: str = "gemini-embedding-001"

    GEMINI_EMBEDDING_DIMENSIONS: int = 768
    GEMINI_GENERATION_MODEL: str = "gemini-3.5-flash"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


settings = Settings()



