from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    app_name: str = "AI DevOps Assistant"
    app_version: str = "1.0"

    database_url: str

    openai_api_key: str

    class Config:
        env_file = ".env"


settings = Settings()