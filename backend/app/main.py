"""
FIRE Brasil App - Backend Principal
Sistema de controle financeiro pessoal para independência financeira
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
import asyncio
import os
from datetime import datetime

import os
from app.core.config import settings
from app.core.mcp_manager import MCPManager
from app.agents.document_processor import DocumentProcessorAgent
from app.agents.expense_categorizer import ExpenseCategorizerAgent
from app.agents.fire_calculator import FireCalculatorAgent
from app.agents.financial_advisor import FinancialAdvisorAgent
from app.schemas.expense import ExpenseCreate, ExpenseResponse
from app.schemas.fire import FireCalculationRequest, FireCalculationResponse
from app.services.database import init_database

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
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gerenciador MCP e Agentes
mcp_manager = MCPManager()
document_processor = DocumentProcessorAgent()
expense_categorizer = ExpenseCategorizerAgent()
fire_calculator = FireCalculatorAgent()
financial_advisor = FinancialAdvisorAgent()

@app.on_event("startup")
async def startup_event():
    """Inicializar serviços na inicialização"""
    await init_database()
    await mcp_manager.initialize()
    print("🚀 FIRE Brasil API iniciada com sucesso!")

@app.on_event("shutdown")
async def shutdown_event():
    """Limpeza na finalização"""
    await mcp_manager.cleanup()
    print("👋 FIRE Brasil API finalizada")

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
        "mcp_status": await mcp_manager.get_status(),
        "timestamp": datetime.now().isoformat()
    }

# === ENDPOINTS DE PROCESSAMENTO DE DOCUMENTOS ===

@app.post("/upload/document", response_model=dict)
async def upload_document(
    file: UploadFile = File(...),
    user_id: str = Form(...)
):
    """
    Upload e processamento de documentos financeiros
    Suporta: PDF, Excel, CSV, imagens
    """
    try:
        # Salvar arquivo temporariamente
        file_path = f"temp_{file.filename}"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Processar documento
        result = await document_processor.process_document(file_path, user_id)
        
        # Limpar arquivo temporário
        os.remove(file_path)
        
        return {
            "success": True,
            "message": "Documento processado com sucesso",
            "data": result
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar documento: {str(e)}")

@app.post("/expenses/categorize", response_model=List[ExpenseResponse])
async def categorize_expenses(
    expenses: List[ExpenseCreate],
    user_id: str = Form(...)
):
    """
    Categorizar gastos automaticamente usando OpenAI
    """
    try:
        categorized_expenses = await expense_categorizer.categorize_batch(expenses, user_id)
        return categorized_expenses
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao categorizar gastos: {str(e)}")

@app.post("/expenses/manual", response_model=ExpenseResponse)
async def add_manual_expense(
    expense: ExpenseCreate,
    user_id: str = Form(...)
):
    """
    Adicionar gasto manual com categorização automática
    """
    try:
        # Categorizar automaticamente
        categorized = await expense_categorizer.categorize_single(expense, user_id)
        
        # Salvar no banco (implementar depois)
        # await expense_service.save_expense(categorized, user_id)
        
        return categorized
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao adicionar gasto: {str(e)}")

# === ENDPOINTS FIRE CALCULATOR ===

@app.post("/fire/calculate", response_model=FireCalculationResponse)
async def calculate_fire(
    request: FireCalculationRequest,
    user_id: str = Form(...)
):
    """
    Calcular projeções FIRE personalizadas
    """
    try:
        result = await fire_calculator.calculate_fire_projections(request, user_id)
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no cálculo FIRE: {str(e)}")

@app.get("/fire/scenarios/{user_id}")
async def get_fire_scenarios(user_id: str):
    """
    Obter cenários FIRE pré-configurados
    """
    try:
        scenarios = await fire_calculator.get_default_scenarios(user_id)
        return scenarios
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter cenários: {str(e)}")

# === ENDPOINTS DE ANÁLISE E INSIGHTS ===

@app.get("/analysis/dashboard/{user_id}")
async def get_dashboard_data(user_id: str):
    """
    Dados do dashboard principal
    """
    try:
        dashboard_data = await financial_advisor.generate_dashboard(user_id)
        return dashboard_data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar dashboard: {str(e)}")

@app.get("/analysis/insights/{user_id}")
async def get_financial_insights(user_id: str):
    """
    Insights financeiros personalizados
    """
    try:
        insights = await financial_advisor.generate_insights(user_id)
        return insights
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar insights: {str(e)}")

@app.get("/analysis/monthly-report/{user_id}")
async def get_monthly_report(user_id: str, month: Optional[str] = None):
    """
    Relatório mensal detalhado
    """
    try:
        report = await financial_advisor.generate_monthly_report(user_id, month)
        return report
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar relatório: {str(e)}")

# === ENDPOINTS DE CONFIGURAÇÃO ===

@app.get("/config/categories")
async def get_expense_categories():
    """
    Obter categorias de gastos brasileiras
    """
    return expense_categorizer.get_brazilian_categories()

@app.get("/config/investment-types")
async def get_investment_types():
    """
    Obter tipos de investimento brasileiros
    """
    return fire_calculator.get_brazilian_investment_types()

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )