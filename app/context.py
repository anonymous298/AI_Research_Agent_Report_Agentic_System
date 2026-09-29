# context.py
from dataclasses import dataclass
import httpx

@dataclass
class AppContext:
    user_id: str
    http: httpx.AsyncClient