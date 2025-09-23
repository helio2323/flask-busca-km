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
        "http://localhost:3000",  # Next.js frontend
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://frontend:3000",   # Container frontend
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
if os.getenv("ENVIRONMENT") == "development" and os.path.exists("/.dockerenv"):
    settings = DockerSettings()
else:
    from .config import settings
