"""
Serviços de banco de dados
"""

import asyncio
import logging
from typing import Dict, Any

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

logger = logging.getLogger(__name__)

Base = declarative_base()

class DatabaseService:
    """Serviço de banco de dados"""
    
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
    
    def initialize(self):
        """Inicializar banco de dados"""
        
        self.engine = create_engine(
            settings.DATABASE_URL,
            connect_args={"check_same_thread": False}  # SQLite only
        )
        
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )
        
        # Criar tabelas
        Base.metadata.create_all(bind=self.engine)
        
        logger.info("Banco de dados inicializado")
    
    def get_session(self):
        """Obter sessão do banco"""
        
        if not self.SessionLocal:
            self.initialize()
        
        return self.SessionLocal()

# Instância global
db_service = DatabaseService()

async def init_database():
    """Inicializar banco de dados assíncrono"""
    
    try:
        db_service.initialize()
        logger.info("✅ Banco de dados inicializado com sucesso")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao inicializar banco: {str(e)}")
        raise

def get_db():
    """Dependency para obter sessão do banco"""
    
    db = db_service.get_session()
    try:
        yield db
    finally:
        db.close()