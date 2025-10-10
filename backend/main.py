from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
import os

from app.core.config import settings
from app.core.database import engine, Base
from app.api import routes, suggestions, history, groups, cache

# Criar tabelas do banco
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown
    pass

# Criar aplicação FastAPI
app = FastAPI(
    title=settings.project_name,
    version="1.0.0",
    description="API para cálculo de rotas e pedágios",
    lifespan=lifespan
)

# Configurar CORS
def get_cors_origins():
    """Obter origens CORS configuradas"""
    origins = settings.backend_cors_origins.copy()
    
    # Adicionar origens extras via variável de ambiente
    if settings.additional_cors_origins:
        additional_origins = settings.additional_cors_origins.split(",")
        origins.extend([origin.strip() for origin in additional_origins])
    
    # Em desenvolvimento, permitir qualquer origem
    if os.getenv("ENVIRONMENT", "development") == "development":
        origins.append("*")
    
    return origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(routes.router, prefix=settings.api_v1_str)
app.include_router(suggestions.router, prefix=settings.api_v1_str)
app.include_router(history.router, prefix=settings.api_v1_str)
app.include_router(groups.router, prefix=settings.api_v1_str)
app.include_router(cache.router, prefix=settings.api_v1_str)

@app.get("/")
async def root():
    return {"message": "Sistema de Cálculo de Rotas API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
