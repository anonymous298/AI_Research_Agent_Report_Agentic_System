# config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    openai_api_key: str
    model: str = "gpt-5-mini"
    max_turns: int = 10

    serper_api_key: str

    langsmith_tracing: str = "true"
    langsmith_endpoint: str = "https://api.smith.langchain.com"
    langsmith_api_key: str = ""
    langsmith_project: str = ""

settings = Settings()