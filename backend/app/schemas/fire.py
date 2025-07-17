"""
Schemas para cálculos FIRE (Financial Independence, Retire Early)
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import date
from decimal import Decimal
from enum import Enum

class FireScenario(str, Enum):
    """Cenários FIRE"""
    LEAN_FIRE = "lean_fire"      # R$ 3.000/mês
    REGULAR_FIRE = "regular_fire"  # R$ 6.000/mês
    FAT_FIRE = "fat_fire"        # R$ 15.000/mês
    COAST_FIRE = "coast_fire"    # Parar de investir, deixar render
    BARISTA_FIRE = "barista_fire" # Trabalho parcial + investimentos

class InvestmentProfile(str, Enum):
    """Perfil de investimento"""
    CONSERVADOR = "conservador"  # 70% renda fixa, 30% variável
    MODERADO = "moderado"        # 50% renda fixa, 50% variável
    AGRESSIVO = "agressivo"      # 30% renda fixa, 70% variável

class FireCalculationRequest(BaseModel):
    """Request para cálculo FIRE"""
    
    # Situação atual
    current_age: int = Field(..., ge=18, le=80, description="Idade atual")
    current_savings: Decimal = Field(..., ge=0, description="Patrimônio atual")
    monthly_income: Decimal = Field(..., gt=0, description="Renda mensal líquida")
    monthly_expenses: Decimal = Field(..., gt=0, description="Gastos mensais")
    
    # Metas
    target_monthly_expenses: Optional[Decimal] = Field(None, description="Gastos mensais na aposentadoria")
    target_age: Optional[int] = Field(None, ge=30, le=80, description="Idade alvo para aposentadoria")
    fire_scenario: FireScenario = Field(default=FireScenario.REGULAR_FIRE, description="Cenário FIRE")
    
    # Investimentos
    investment_profile: InvestmentProfile = Field(default=InvestmentProfile.MODERADO, description="Perfil de investimento")
    expected_return: Optional[Decimal] = Field(None, description="Retorno esperado anual (decimal)")
    
    # Configurações brasileiras
    inflation_rate: Optional[Decimal] = Field(None, description="Taxa de inflação (IPCA)")
    consider_tax: bool = Field(default=True, description="Considerar impostos")
    
    @validator('monthly_expenses')
    def validate_expenses_vs_income(cls, v, values):
        """Validar que gastos não excedam renda"""
        if 'monthly_income' in values and v >= values['monthly_income']:
            raise ValueError('Gastos mensais devem ser menores que a renda')
        return v
    
    @validator('target_age')
    def validate_target_age(cls, v, values):
        """Validar idade alvo"""
        if v and 'current_age' in values and v <= values['current_age']:
            raise ValueError('Idade alvo deve ser maior que idade atual')
        return v

class FireProjection(BaseModel):
    """Projeção FIRE"""
    year: int = Field(..., description="Ano")
    age: int = Field(..., description="Idade")
    accumulated_amount: Decimal = Field(..., description="Valor acumulado")
    monthly_contribution: Decimal = Field(..., description="Aporte mensal")
    annual_return: Decimal = Field(..., description="Retorno anual")
    inflation_adjusted: Decimal = Field(..., description="Valor corrigido pela inflação")
    
class FireCalculationResponse(BaseModel):
    """Resposta do cálculo FIRE"""
    
    # Resultados principais
    fire_number: Decimal = Field(..., description="Número FIRE (25x gastos)")
    years_to_fire: int = Field(..., description="Anos para atingir FIRE")
    target_age: int = Field(..., description="Idade quando atingir FIRE")
    monthly_savings_needed: Decimal = Field(..., description="Poupança mensal necessária")
    savings_rate: Decimal = Field(..., description="Taxa de poupança necessária")
    
    # Projeções
    projections: List[FireProjection] = Field(..., description="Projeções anuais")
    
    # Cenários
    scenarios: Dict[str, Dict[str, Any]] = Field(..., description="Diferentes cenários")
    
    # Configurações usadas
    assumptions: Dict[str, Any] = Field(..., description="Premissas do cálculo")
    
    # Insights
    insights: List[str] = Field(..., description="Insights e recomendações")
    warnings: List[str] = Field(..., description="Alertas e considerações")

class FireScenarioComparison(BaseModel):
    """Comparação entre cenários FIRE"""
    scenario: FireScenario = Field(..., description="Cenário")
    monthly_target: Decimal = Field(..., description="Gasto mensal alvo")
    fire_number: Decimal = Field(..., description="Número FIRE")
    years_to_achieve: int = Field(..., description="Anos para atingir")
    monthly_savings_needed: Decimal = Field(..., description="Poupança mensal necessária")
    savings_rate: Decimal = Field(..., description="Taxa de poupança")
    feasibility: str = Field(..., description="Viabilidade (fácil/moderado/difícil)")

class FireOptimization(BaseModel):
    """Otimização FIRE"""
    
    # Análise atual
    current_savings_rate: Decimal = Field(..., description="Taxa de poupança atual")
    current_fire_timeline: int = Field(..., description="Anos com situação atual")
    
    # Otimizações possíveis
    expense_reduction_impact: Dict[str, Any] = Field(..., description="Impacto da redução de gastos")
    income_increase_impact: Dict[str, Any] = Field(..., description="Impacto do aumento de renda")
    investment_optimization: Dict[str, Any] = Field(..., description="Otimização de investimentos")
    
    # Recomendações
    recommendations: List[Dict[str, Any]] = Field(..., description="Recomendações específicas")
    
class FireDashboard(BaseModel):
    """Dashboard FIRE"""
    
    # Status atual
    current_progress: Decimal = Field(..., description="Progresso atual (%)")
    fire_number: Decimal = Field(..., description="Número FIRE alvo")
    current_net_worth: Decimal = Field(..., description="Patrimônio atual")
    
    # Projeções
    years_remaining: int = Field(..., description="Anos restantes")
    monthly_progress: Decimal = Field(..., description="Progresso mensal")
    
    # Métricas
    savings_rate: Decimal = Field(..., description="Taxa de poupança")
    fire_date: date = Field(..., description="Data estimada para FIRE")
    
    # Breakdown
    progress_by_category: Dict[str, Decimal] = Field(..., description="Progresso por categoria")
    
class CoastFireCalculation(BaseModel):
    """Cálculo Coast FIRE"""
    
    coast_fire_number: Decimal = Field(..., description="Valor para Coast FIRE")
    coast_fire_age: int = Field(..., description="Idade para atingir Coast FIRE")
    years_to_coast: int = Field(..., description="Anos para Coast FIRE")
    
    # Após Coast FIRE
    no_savings_needed_from: int = Field(..., description="Idade quando não precisa mais poupar")
    final_amount_at_65: Decimal = Field(..., description="Valor final aos 65 anos")
    
class BaristaFireCalculation(BaseModel):
    """Cálculo Barista FIRE"""
    
    barista_fire_number: Decimal = Field(..., description="Valor para Barista FIRE")
    barista_fire_age: int = Field(..., description="Idade para Barista FIRE")
    part_time_income_needed: Decimal = Field(..., description="Renda parcial necessária")
    
    # Simulações
    work_scenarios: List[Dict[str, Any]] = Field(..., description="Cenários de trabalho parcial")

class FireStressTest(BaseModel):
    """Teste de estresse FIRE"""
    
    # Cenários de crise
    market_crash_impact: Dict[str, Any] = Field(..., description="Impacto de crash do mercado")
    high_inflation_impact: Dict[str, Any] = Field(..., description="Impacto de alta inflação")
    income_loss_impact: Dict[str, Any] = Field(..., description="Impacto de perda de renda")
    
    # Estratégias de contingência
    contingency_strategies: List[str] = Field(..., description="Estratégias de contingência")
    
    # Margem de segurança
    safety_margin: Decimal = Field(..., description="Margem de segurança recomendada")

class FireEducationContent(BaseModel):
    """Conteúdo educativo FIRE"""
    
    # Conceitos
    fire_explanation: str = Field(..., description="Explicação do movimento FIRE")
    rule_of_25: str = Field(..., description="Explicação da regra 25x")
    four_percent_rule: str = Field(..., description="Explicação da regra 4%")
    
    # Estratégias brasileiras
    brazilian_strategies: List[str] = Field(..., description="Estratégias específicas do Brasil")
    investment_options: List[Dict[str, Any]] = Field(..., description="Opções de investimento")
    
    # Dicas
    tips: List[str] = Field(..., description="Dicas práticas")
    common_mistakes: List[str] = Field(..., description="Erros comuns")

class FireGoalTracking(BaseModel):
    """Acompanhamento de metas FIRE"""
    
    # Metas
    short_term_goals: List[Dict[str, Any]] = Field(..., description="Metas de curto prazo")
    medium_term_goals: List[Dict[str, Any]] = Field(..., description="Metas de médio prazo")
    long_term_goals: List[Dict[str, Any]] = Field(..., description="Metas de longo prazo")
    
    # Progresso
    goals_progress: Dict[str, Decimal] = Field(..., description="Progresso das metas")
    
    # Marcos
    milestones: List[Dict[str, Any]] = Field(..., description="Marcos importantes")
    next_milestone: Dict[str, Any] = Field(..., description="Próximo marco")