from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PORT: int = 8000
    HOST: str = "127.0.0.1"

    ALLOW_ORIGINS: list[str] = ["*"]

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
