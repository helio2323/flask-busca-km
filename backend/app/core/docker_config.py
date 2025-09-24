from pydantic_settings import BaseSettings
from typing import Optional
import os

class DockerSettings(BaseSettings):
    # Database - Configuração para Docker
    database_url: str = "postgresql://postgres:postgres@postgres:5432/rotas_db"
    
    # API
    api_v1_str: str = "/api/v1"
    project_name: str = "Sistema de Cálculo de Rotas"
    
    # CORS - Configuração para Docker
    backend_cors_origins: list = [
        "http://localhost:5000",  # Next.js frontend
        "http://localhost:5001",  # Next.js frontend dev
        "http://127.0.0.1:5000",
        "http://127.0.0.1:5001",
        "http://frontend:5000",   # Container frontend
    ]
    
    # Cache settings
    cache_expiration_hours: int = 6
    coordinates_cache_expiration_hours: int = 168  # 7 days
    
    # External APIs
    rotas_brasil_api_url: str = "https://rotasbrasil.com.br/roterizador/buscaRota/"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Usar configuração Docker se estiver em container
if os.path.exists("/.dockerenv") or os.getenv("ENVIRONMENT") == "development":
    settings = DockerSettings()
else:
    from .config import settings
