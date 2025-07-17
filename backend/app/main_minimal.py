"""
FIRE Brasil App - Backend Principal (Versão Minimal)
Sistema de controle financeiro pessoal para independência financeira
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os

# Configuração básica
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://fire-brasil.vercel.app",
    "https://*.vercel.app"
]

# Inicializar aplicação
app = FastAPI(
    title="FIRE Brasil API",
    description="API para controle financeiro pessoal e independência financeira",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "🇧🇷 FIRE Brasil API",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Verificação de saúde da API"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

# Endpoints básicos de teste
@app.get("/test")
async def test_endpoint():
    """Endpoint de teste"""
    return {"message": "API funcionando!", "status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)