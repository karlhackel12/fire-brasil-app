"""
Schemas para expenses (gastos/despesas)
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from decimal import Decimal
from enum import Enum

class ExpenseType(str, Enum):
    """Tipos de despesas"""
    EXPENSE = "expense"
    INCOME = "income"

class ExpenseCategory(str, Enum):
    """Categorias de despesas brasileiras"""
    ALIMENTACAO = "alimentacao"
    MORADIA = "moradia"
    TRANSPORTE = "transporte"
    SAUDE = "saude"
    EDUCACAO = "educacao"
    LAZER = "lazer"
    VESTUARIO = "vestuario"
    FINANCEIRO = "financeiro"
    OUTROS = "outros"

class PaymentMethod(str, Enum):
    """Métodos de pagamento"""
    DINHEIRO = "dinheiro"
    DEBITO = "debito"
    CREDITO = "credito"
    PIX = "pix"
    BOLETO = "boleto"
    TRANSFERENCIA = "transferencia"

class ExpenseBase(BaseModel):
    """Base para expense"""
    date: date = Field(..., description="Data da despesa")
    description: str = Field(..., min_length=1, max_length=255, description="Descrição da despesa")
    amount: Decimal = Field(..., gt=0, description="Valor da despesa")
    type: ExpenseType = Field(default=ExpenseType.EXPENSE, description="Tipo da transação")
    category: Optional[ExpenseCategory] = Field(None, description="Categoria da despesa")
    subcategory: Optional[str] = Field(None, max_length=100, description="Subcategoria")
    payment_method: Optional[PaymentMethod] = Field(None, description="Método de pagamento")
    tags: Optional[List[str]] = Field(default=[], description="Tags personalizadas")
    notes: Optional[str] = Field(None, max_length=500, description="Notas adicionais")
    
    @validator('amount')
    def validate_amount(cls, v):
        """Validar valor"""
        if v <= 0:
            raise ValueError('Valor deve ser maior que zero')
        return v
    
    @validator('description')
    def validate_description(cls, v):
        """Validar descrição"""
        if not v or v.strip() == "":
            raise ValueError('Descrição não pode estar vazia')
        return v.strip()

class ExpenseCreate(ExpenseBase):
    """Schema para criação de expense"""
    pass

class ExpenseUpdate(BaseModel):
    """Schema para atualização de expense"""
    date: Optional[date] = None
    description: Optional[str] = Field(None, min_length=1, max_length=255)
    amount: Optional[Decimal] = Field(None, gt=0)
    type: Optional[ExpenseType] = None
    category: Optional[ExpenseCategory] = None
    subcategory: Optional[str] = Field(None, max_length=100)
    payment_method: Optional[PaymentMethod] = None
    tags: Optional[List[str]] = None
    notes: Optional[str] = Field(None, max_length=500)

class ExpenseResponse(ExpenseBase):
    """Schema de resposta para expense"""
    id: int = Field(..., description="ID da despesa")
    user_id: str = Field(..., description="ID do usuário")
    created_at: datetime = Field(..., description="Data de criação")
    updated_at: Optional[datetime] = Field(None, description="Data de atualização")
    
    # Dados da IA
    ai_confidence: Optional[float] = Field(None, ge=0, le=1, description="Confiança da IA na categorização")
    ai_suggested_category: Optional[str] = Field(None, description="Categoria sugerida pela IA")
    ai_reasoning: Optional[str] = Field(None, description="Raciocínio da IA")
    
    class Config:
        from_attributes = True

class ExpenseBatch(BaseModel):
    """Schema para lote de expenses"""
    expenses: List[ExpenseCreate] = Field(..., description="Lista de despesas")
    user_id: str = Field(..., description="ID do usuário")
    
    @validator('expenses')
    def validate_expenses(cls, v):
        """Validar lista de despesas"""
        if not v:
            raise ValueError('Lista de despesas não pode estar vazia')
        if len(v) > 100:
            raise ValueError('Máximo de 100 despesas por lote')
        return v

class ExpenseStats(BaseModel):
    """Estatísticas de despesas"""
    total_expenses: Decimal = Field(..., description="Total de despesas")
    total_income: Decimal = Field(..., description="Total de receitas")
    net_amount: Decimal = Field(..., description="Valor líquido")
    expense_count: int = Field(..., description="Número de despesas")
    income_count: int = Field(..., description="Número de receitas")
    
    # Por categoria
    by_category: Dict[str, Decimal] = Field(default={}, description="Gastos por categoria")
    by_payment_method: Dict[str, Decimal] = Field(default={}, description="Gastos por método")
    by_month: Dict[str, Decimal] = Field(default={}, description="Gastos por mês")
    
    # Médias
    average_expense: Decimal = Field(..., description="Gasto médio")
    average_income: Decimal = Field(..., description="Receita média")

class ExpenseFilter(BaseModel):
    """Filtros para consulta de despesas"""
    start_date: Optional[date] = Field(None, description="Data inicial")
    end_date: Optional[date] = Field(None, description="Data final")
    category: Optional[ExpenseCategory] = Field(None, description="Categoria")
    subcategory: Optional[str] = Field(None, description="Subcategoria")
    payment_method: Optional[PaymentMethod] = Field(None, description="Método de pagamento")
    type: Optional[ExpenseType] = Field(None, description="Tipo")
    min_amount: Optional[Decimal] = Field(None, gt=0, description="Valor mínimo")
    max_amount: Optional[Decimal] = Field(None, gt=0, description="Valor máximo")
    tags: Optional[List[str]] = Field(None, description="Tags")
    search: Optional[str] = Field(None, description="Busca na descrição")
    
    @validator('end_date')
    def validate_date_range(cls, v, values):
        """Validar intervalo de datas"""
        if v and 'start_date' in values and values['start_date']:
            if v < values['start_date']:
                raise ValueError('Data final deve ser maior que data inicial')
        return v
    
    @validator('max_amount')
    def validate_amount_range(cls, v, values):
        """Validar intervalo de valores"""
        if v and 'min_amount' in values and values['min_amount']:
            if v < values['min_amount']:
                raise ValueError('Valor máximo deve ser maior que valor mínimo')
        return v

class ExpenseList(BaseModel):
    """Lista paginada de despesas"""
    items: List[ExpenseResponse] = Field(..., description="Lista de despesas")
    total: int = Field(..., description="Total de itens")
    page: int = Field(..., description="Página atual")
    per_page: int = Field(..., description="Itens por página")
    pages: int = Field(..., description="Total de páginas")
    
class ExpenseImportResult(BaseModel):
    """Resultado da importação de despesas"""
    success: bool = Field(..., description="Sucesso da importação")
    imported_count: int = Field(..., description="Número de despesas importadas")
    failed_count: int = Field(..., description="Número de falhas")
    duplicates_count: int = Field(..., description="Número de duplicatas")
    errors: List[str] = Field(default=[], description="Lista de erros")
    warnings: List[str] = Field(default=[], description="Lista de avisos")
    imported_expenses: List[ExpenseResponse] = Field(default=[], description="Despesas importadas")

class ExpenseAnalysis(BaseModel):
    """Análise de despesas"""
    period: str = Field(..., description="Período analisado")
    total_spent: Decimal = Field(..., description="Total gasto")
    total_earned: Decimal = Field(..., description="Total recebido")
    savings_rate: float = Field(..., description="Taxa de poupança")
    
    # Tendências
    trend: str = Field(..., description="Tendência (increasing/decreasing/stable)")
    trend_percentage: float = Field(..., description="Percentual da tendência")
    
    # Insights
    insights: List[str] = Field(default=[], description="Insights da análise")
    recommendations: List[str] = Field(default=[], description="Recomendações")
    
    # Projeções
    monthly_projection: Decimal = Field(..., description="Projeção mensal")
    yearly_projection: Decimal = Field(..., description="Projeção anual")