# config.py
import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv(override=True)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra='ignore')
    openai_api_key: str
    model: str = "gpt-5-mini"
    embedding_model: str = "text-embedding-3-small"
    max_turns: int = 10

    serper_api_key: str

    # database_url: str = "postgresql+asyncpg://postgres:postgresql123@localhost:5432/research_agent" #locla
    database_url: str = os.getenv("PG_CONNECTION_STRING")

    langsmith_tracing: str = "true"
    langsmith_endpoint: str = "https://api.smith.langchain.com"
    langsmith_api_key: str = os.getenv("LANGSMITH_API_KEY")
    langsmith_project: str = "AI_Research_Report_Agent"

settings = Settings()