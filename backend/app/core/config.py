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
        "http://localhost:3000",  # Next.js frontend padrão
        "http://localhost:5000",  # Next.js frontend (nova porta)
        "http://localhost:5001",  # Next.js frontend dev
        "http://localhost:50001", # Next.js frontend atual
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5000",  # Nova porta frontend
        "http://127.0.0.1:5001",
        "http://127.0.0.1:50001",
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
