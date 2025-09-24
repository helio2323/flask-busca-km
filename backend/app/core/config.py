from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./rotas.db"
    
    # API
    api_v1_str: str = "/api/v1"
    project_name: str = "Sistema de Cálculo de Rotas"
    
    # CORS
    backend_cors_origins: list = [
        "http://localhost:5000",  # Next.js frontend
        "http://localhost:5001",  # Next.js frontend dev
        "http://127.0.0.1:5000",
        "http://127.0.0.1:5001",
    ]
    
    # Cache settings
    cache_expiration_hours: int = 6
    coordinates_cache_expiration_hours: int = 168  # 7 days
    
    # External APIs
    rotas_brasil_api_url: str = "https://rotasbrasil.com.br/roterizador/buscaRota/"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
