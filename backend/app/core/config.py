"""
Configurações da aplicação FIRE Brasil
"""

from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # Configurações da API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FIRE Brasil"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Sistema de controle financeiro pessoal para independência financeira"
    
    # Configurações de CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ]
    
    # Configurações de banco de dados
    DATABASE_URL: str = "sqlite:///./fire_brasil.db"
    
    # Configurações OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = "gpt-4o"
    OPENAI_TEMPERATURE: float = 0.3
    
    # Configurações de upload
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_FOLDER: str = "uploads"
    ALLOWED_EXTENSIONS: List[str] = [
        ".pdf", ".xlsx", ".xls", ".csv", 
        ".jpg", ".jpeg", ".png", ".txt"
    ]
    
    # Configurações MCP
    MCP_SERVERS: dict = {
        "document_processor": {
            "command": "python",
            "args": ["-m", "app.mcp_servers.document_processor"]
        },
        "expense_categorizer": {
            "command": "python", 
            "args": ["-m", "app.mcp_servers.expense_categorizer"]
        },
        "fire_calculator": {
            "command": "python",
            "args": ["-m", "app.mcp_servers.fire_calculator"]
        },
        "financial_advisor": {
            "command": "python",
            "args": ["-m", "app.mcp_servers.financial_advisor"]
        }
    }
    
    # Configurações brasileiras
    BRAZILIAN_CURRENCY: str = "BRL"
    BRAZILIAN_LOCALE: str = "pt_BR"
    INFLATION_INDEX: str = "IPCA"
    DEFAULT_INVESTMENT_RETURN: float = 0.10  # 10% ao ano
    FIRE_WITHDRAWAL_RATE: float = 0.04  # 4% ao ano
    FIRE_MULTIPLIER: int = 25  # 25x gastos anuais
    
    # Configurações de segurança
    SECRET_KEY: str = os.getenv("SECRET_KEY", "fire-brasil-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Configurações de logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Configurações de desenvolvimento
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    TESTING: bool = os.getenv("TESTING", "false").lower() == "true"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

# Instância global das configurações
settings = Settings()

# Categorias de gastos brasileiras
BRAZILIAN_EXPENSE_CATEGORIES = {
    "alimentacao": {
        "name": "Alimentação",
        "icon": "🍽️",
        "subcategories": [
            "supermercado", "restaurante", "lanche", "delivery", 
            "padaria", "açougue", "bebidas", "doces"
        ]
    },
    "moradia": {
        "name": "Moradia",
        "icon": "🏠",
        "subcategories": [
            "aluguel", "condominio", "iptu", "luz", "agua", 
            "gas", "internet", "telefone", "limpeza", "reparos"
        ]
    },
    "transporte": {
        "name": "Transporte",
        "icon": "🚗",
        "subcategories": [
            "combustivel", "uber", "onibus", "metro", "taxi",
            "estacionamento", "pedagio", "manutencao", "seguro", "ipva"
        ]
    },
    "saude": {
        "name": "Saúde",
        "icon": "💊",
        "subcategories": [
            "plano_saude", "medico", "dentista", "exames", 
            "farmacia", "academia", "terapia", "veterinario"
        ]
    },
    "educacao": {
        "name": "Educação",
        "icon": "📚",
        "subcategories": [
            "escola", "faculdade", "curso", "livros", 
            "material_escolar", "aulas_particulares"
        ]
    },
    "lazer": {
        "name": "Lazer",
        "icon": "🎬",
        "subcategories": [
            "cinema", "teatro", "shows", "viagem", "restaurante",
            "streaming", "jogos", "hobbies", "presentes"
        ]
    },
    "vestuario": {
        "name": "Vestuário",
        "icon": "👕",
        "subcategories": [
            "roupas", "sapatos", "acessorios", "cosmeticos", 
            "cabelo", "limpeza_a_seco"
        ]
    },
    "financeiro": {
        "name": "Financeiro",
        "icon": "💰",
        "subcategories": [
            "investimentos", "emprestimo", "cartao_credito", 
            "tarifas_bancarias", "seguros", "previdencia"
        ]
    },
    "outros": {
        "name": "Outros",
        "icon": "📦",
        "subcategories": [
            "diversos", "emergencia", "caridade", "impostos"
        ]
    }
}

# Tipos de investimento brasileiros
BRAZILIAN_INVESTMENT_TYPES = {
    "renda_fixa": {
        "name": "Renda Fixa",
        "types": [
            {"name": "Tesouro Selic", "risk": "baixo", "liquidity": "alta"},
            {"name": "Tesouro IPCA+", "risk": "baixo", "liquidity": "media"},
            {"name": "CDB", "risk": "baixo", "liquidity": "media"},
            {"name": "LCI/LCA", "risk": "baixo", "liquidity": "baixa"},
            {"name": "Poupança", "risk": "baixo", "liquidity": "alta"}
        ]
    },
    "renda_variavel": {
        "name": "Renda Variável",
        "types": [
            {"name": "Ações", "risk": "alto", "liquidity": "alta"},
            {"name": "FIIs", "risk": "medio", "liquidity": "alta"},
            {"name": "ETFs", "risk": "medio", "liquidity": "alta"},
            {"name": "Fundos Multimercado", "risk": "alto", "liquidity": "media"}
        ]
    },
    "previdencia": {
        "name": "Previdência",
        "types": [
            {"name": "PGBL", "risk": "variavel", "liquidity": "baixa"},
            {"name": "VGBL", "risk": "variavel", "liquidity": "baixa"}
        ]
    }
}