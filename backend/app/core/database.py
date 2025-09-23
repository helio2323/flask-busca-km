from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Criar engine do SQLAlchemy
engine = create_engine(settings.database_url)

# Criar SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()

# Dependency para obter sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
