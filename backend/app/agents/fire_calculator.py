"""
Agente Calculadora FIRE
Responsável por calcular projeções de independência financeira adaptadas ao Brasil
"""

import math
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, date
from decimal import Decimal, ROUND_HALF_UP

from openai import AsyncOpenAI

from app.core.config import settings, BRAZILIAN_INVESTMENT_TYPES
from app.schemas.fire import (
    FireCalculationRequest, FireCalculationResponse, FireProjection,
    FireScenario, InvestmentProfile, FireScenarioComparison,
    FireOptimization, CoastFireCalculation, BaristaFireCalculation
)

logger = logging.getLogger(__name__)

class FireCalculatorAgent:
    """Agente para cálculos FIRE brasileiros"""
    
    def __init__(self):
        self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.investment_types = BRAZILIAN_INVESTMENT_TYPES
        
        # Configurações brasileiras
        self.default_inflation = Decimal('0.045')  # 4.5% IPCA
        self.default_returns = {
            InvestmentProfile.CONSERVADOR: Decimal('0.08'),   # 8% ao ano
            InvestmentProfile.MODERADO: Decimal('0.10'),      # 10% ao ano
            InvestmentProfile.AGRESSIVO: Decimal('0.12'),     # 12% ao ano
        }
        
        # Cenários FIRE brasileiros
        self.fire_scenarios = {
            FireScenario.LEAN_FIRE: Decimal('3000'),     # R$ 3.000/mês
            FireScenario.REGULAR_FIRE: Decimal('6000'),   # R$ 6.000/mês
            FireScenario.FAT_FIRE: Decimal('15000'),     # R$ 15.000/mês
        }
    
    async def calculate_fire_projections(self, request: FireCalculationRequest, user_id: str) -> FireCalculationResponse:
        """
        Calcular projeções FIRE completas
        
        Args:
            request: Dados para cálculo
            user_id: ID do usuário
            
        Returns:
            Projeções FIRE completas
        """
        try:
            # Calcular configurações
            assumptions = self._calculate_assumptions(request)
            
            # Calcular número FIRE
            fire_number = self._calculate_fire_number(request, assumptions)
            
            # Calcular tempo para FIRE
            years_to_fire, monthly_savings_needed = self._calculate_time_to_fire(
                request, fire_number, assumptions
            )
            
            # Gerar projeções anuais
            projections = self._generate_projections(
                request, fire_number, years_to_fire, monthly_savings_needed, assumptions
            )
            
            # Calcular cenários alternativos
            scenarios = await self._calculate_scenarios(request, user_id)
            
            # Gerar insights
            insights = await self._generate_insights(request, years_to_fire, monthly_savings_needed, user_id)
            
            # Gerar warnings
            warnings = self._generate_warnings(request, years_to_fire, monthly_savings_needed)
            
            # Calcular taxa de poupança
            savings_rate = (monthly_savings_needed / request.monthly_income) * 100
            
            response = FireCalculationResponse(
                fire_number=fire_number,
                years_to_fire=years_to_fire,
                target_age=request.current_age + years_to_fire,
                monthly_savings_needed=monthly_savings_needed,
                savings_rate=savings_rate,
                projections=projections,
                scenarios=scenarios,
                assumptions=assumptions,
                insights=insights,
                warnings=warnings
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Erro no cálculo FIRE: {str(e)}")
            raise
    
    def _calculate_assumptions(self, request: FireCalculationRequest) -> Dict[str, Any]:
        """Calcular premissas do cálculo"""
        
        # Taxa de retorno baseada no perfil
        expected_return = request.expected_return or self.default_returns[request.investment_profile]
        
        # Taxa de inflação
        inflation_rate = request.inflation_rate or self.default_inflation
        
        # Gastos mensais alvo
        target_expenses = request.target_monthly_expenses or request.monthly_expenses
        
        # Taxa real de retorno (descontando inflação)
        real_return = (1 + expected_return) / (1 + inflation_rate) - 1
        
        return {
            "expected_return": float(expected_return),
            "inflation_rate": float(inflation_rate),
            "real_return": float(real_return),
            "target_monthly_expenses": float(target_expenses),
            "fire_multiplier": 25,  # Regra 25x
            "withdrawal_rate": 0.04,  # Regra 4%
            "consider_tax": request.consider_tax
        }
    
    def _calculate_fire_number(self, request: FireCalculationRequest, assumptions: Dict[str, Any]) -> Decimal:
        """Calcular número FIRE (25x gastos anuais)"""
        
        target_expenses = Decimal(str(assumptions["target_monthly_expenses"]))
        annual_expenses = target_expenses * 12
        
        # Regra 25x
        fire_number = annual_expenses * assumptions["fire_multiplier"]
        
        # Ajustar para impostos se necessário
        if assumptions["consider_tax"]:
            # Considerar IR sobre rendimentos (aproximadamente 15%)
            fire_number = fire_number * Decimal('1.15')
        
        return fire_number.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    def _calculate_time_to_fire(self, request: FireCalculationRequest, fire_number: Decimal, assumptions: Dict[str, Any]) -> Tuple[int, Decimal]:
        """Calcular tempo para FIRE e poupança necessária"""
        
        current_savings = request.current_savings
        monthly_income = request.monthly_income
        monthly_expenses = request.monthly_expenses
        
        # Capacidade máxima de poupança
        max_monthly_savings = monthly_income - monthly_expenses
        
        if max_monthly_savings <= 0:
            raise ValueError("Renda insuficiente para poupança")
        
        # Taxa de retorno mensal
        monthly_return = (1 + Decimal(str(assumptions["expected_return"]))) ** (Decimal('1') / Decimal('12')) - 1
        
        # Calcular usando fórmula de valor futuro da anuidade
        # FV = PV * (1 + r)^n + PMT * [((1 + r)^n - 1) / r]
        # Resolvendo para n (número de meses)
        
        pv = current_savings
        fv = fire_number
        r = monthly_return
        
        # Se não há poupança atual, usar fórmula simples
        if pv == 0:
            # FV = PMT * [((1 + r)^n - 1) / r]
            # Resolvendo para n
            monthly_savings = max_monthly_savings * Decimal('0.7')  # 70% da capacidade
            
            if monthly_savings * 12 * 25 < fire_number:  # Verificação rápida
                monthly_savings = max_monthly_savings * Decimal('0.9')  # 90% da capacidade
            
            # Cálculo iterativo para encontrar n
            months = self._solve_for_months(fv, monthly_savings, r)
            
        else:
            # Com poupança inicial
            monthly_savings = max_monthly_savings * Decimal('0.7')
            months = self._solve_for_months_with_pv(fv, pv, monthly_savings, r)
        
        years = math.ceil(months / 12)
        
        return years, monthly_savings.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    def _solve_for_months(self, fv: Decimal, pmt: Decimal, r: Decimal) -> int:
        """Resolver para número de meses usando método iterativo"""
        
        if r == 0:
            return int(fv / pmt)
        
        # Usar logaritmo para resolver
        # n = log(1 + (FV * r) / PMT) / log(1 + r)
        try:
            numerator = 1 + (fv * r) / pmt
            if numerator <= 0:
                raise ValueError("Valor futuro muito alto para a poupança mensal")
            
            months = math.log(float(numerator)) / math.log(float(1 + r))
            return max(1, int(months))
            
        except (ValueError, ZeroDivisionError):
            # Fallback para método iterativo
            return self._iterative_solve(fv, pmt, r)
    
    def _solve_for_months_with_pv(self, fv: Decimal, pv: Decimal, pmt: Decimal, r: Decimal) -> int:
        """Resolver para meses com valor presente"""
        
        # Método iterativo
        months = 0
        current_value = pv
        
        while current_value < fv and months < 600:  # Máximo 50 anos
            current_value = current_value * (1 + r) + pmt
            months += 1
        
        return months
    
    def _iterative_solve(self, fv: Decimal, pmt: Decimal, r: Decimal) -> int:
        """Método iterativo para resolver equação"""
        
        months = 0
        current_value = Decimal('0')
        
        while current_value < fv and months < 600:  # Máximo 50 anos
            current_value = current_value * (1 + r) + pmt
            months += 1
        
        return months
    
    def _generate_projections(self, request: FireCalculationRequest, fire_number: Decimal, 
                            years_to_fire: int, monthly_savings: Decimal, 
                            assumptions: Dict[str, Any]) -> List[FireProjection]:
        """Gerar projeções anuais"""
        
        projections = []
        current_value = request.current_savings
        monthly_return = (1 + Decimal(str(assumptions["expected_return"]))) ** (Decimal('1') / Decimal('12')) - 1
        
        for year in range(1, years_to_fire + 1):
            # Calcular valor no final do ano
            for month in range(12):
                current_value = current_value * (1 + monthly_return) + monthly_savings
            
            # Ajustar pela inflação
            inflation_factor = (1 + Decimal(str(assumptions["inflation_rate"]))) ** year
            inflation_adjusted = current_value / inflation_factor
            
            projection = FireProjection(
                year=datetime.now().year + year,
                age=request.current_age + year,
                accumulated_amount=current_value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                monthly_contribution=monthly_savings,
                annual_return=Decimal(str(assumptions["expected_return"])) * 100,
                inflation_adjusted=inflation_adjusted.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            )
            
            projections.append(projection)
        
        return projections
    
    async def _calculate_scenarios(self, request: FireCalculationRequest, user_id: str) -> Dict[str, Any]:
        """Calcular cenários alternativos"""
        
        scenarios = {}
        
        # Cenários FIRE
        for scenario, monthly_target in self.fire_scenarios.items():
            scenario_request = FireCalculationRequest(
                current_age=request.current_age,
                current_savings=request.current_savings,
                monthly_income=request.monthly_income,
                monthly_expenses=request.monthly_expenses,
                target_monthly_expenses=monthly_target,
                investment_profile=request.investment_profile,
                expected_return=request.expected_return,
                inflation_rate=request.inflation_rate,
                consider_tax=request.consider_tax
            )
            
            try:
                assumptions = self._calculate_assumptions(scenario_request)
                fire_number = self._calculate_fire_number(scenario_request, assumptions)
                years, monthly_savings = self._calculate_time_to_fire(scenario_request, fire_number, assumptions)
                
                scenarios[scenario.value] = {
                    "fire_number": float(fire_number),
                    "years_to_fire": years,
                    "monthly_savings_needed": float(monthly_savings),
                    "monthly_target": float(monthly_target),
                    "savings_rate": float((monthly_savings / request.monthly_income) * 100)
                }
                
            except Exception as e:
                scenarios[scenario.value] = {
                    "error": str(e),
                    "feasible": False
                }
        
        # Coast FIRE
        coast_fire = self._calculate_coast_fire(request)
        scenarios["coast_fire"] = coast_fire
        
        # Barista FIRE
        barista_fire = self._calculate_barista_fire(request)
        scenarios["barista_fire"] = barista_fire
        
        return scenarios
    
    def _calculate_coast_fire(self, request: FireCalculationRequest) -> Dict[str, Any]:
        """Calcular Coast FIRE"""
        
        try:
            # Valor necessário para Coast FIRE aos 65 anos
            target_age = 65
            years_to_65 = target_age - request.current_age
            
            if years_to_65 <= 0:
                return {"error": "Idade já passou dos 65 anos"}
            
            # Valor necessário hoje para atingir FIRE aos 65
            assumptions = self._calculate_assumptions(request)
            fire_number = self._calculate_fire_number(request, assumptions)
            
            # Valor presente necessário
            annual_return = Decimal(str(assumptions["expected_return"]))
            coast_fire_number = fire_number / ((1 + annual_return) ** years_to_65)
            
            # Tempo para atingir Coast FIRE
            if request.current_savings >= coast_fire_number:
                years_to_coast = 0
            else:
                needed_amount = coast_fire_number - request.current_savings
                monthly_savings = request.monthly_income - request.monthly_expenses
                
                if monthly_savings <= 0:
                    return {"error": "Sem capacidade de poupança"}
                
                monthly_return = (1 + annual_return) ** (Decimal('1') / Decimal('12')) - 1
                months = self._solve_for_months(needed_amount, monthly_savings, monthly_return)
                years_to_coast = math.ceil(months / 12)
            
            return {
                "coast_fire_number": float(coast_fire_number),
                "coast_fire_age": request.current_age + years_to_coast,
                "years_to_coast": years_to_coast,
                "final_amount_at_65": float(fire_number)
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def _calculate_barista_fire(self, request: FireCalculationRequest) -> Dict[str, Any]:
        """Calcular Barista FIRE"""
        
        try:
            # Barista FIRE = 50% do FIRE number + renda parcial
            assumptions = self._calculate_assumptions(request)
            full_fire_number = self._calculate_fire_number(request, assumptions)
            barista_fire_number = full_fire_number * Decimal('0.5')
            
            # Renda parcial necessária
            annual_expenses = Decimal(str(assumptions["target_monthly_expenses"])) * 12
            annual_passive_income = barista_fire_number * Decimal('0.04')
            part_time_income_needed = (annual_expenses - annual_passive_income) / 12
            
            # Tempo para Barista FIRE
            if request.current_savings >= barista_fire_number:
                years_to_barista = 0
            else:
                needed_amount = barista_fire_number - request.current_savings
                monthly_savings = request.monthly_income - request.monthly_expenses
                
                if monthly_savings <= 0:
                    return {"error": "Sem capacidade de poupança"}
                
                annual_return = Decimal(str(assumptions["expected_return"]))
                monthly_return = (1 + annual_return) ** (Decimal('1') / Decimal('12')) - 1
                months = self._solve_for_months(needed_amount, monthly_savings, monthly_return)
                years_to_barista = math.ceil(months / 12)
            
            return {
                "barista_fire_number": float(barista_fire_number),
                "barista_fire_age": request.current_age + years_to_barista,
                "years_to_barista": years_to_barista,
                "part_time_income_needed": float(part_time_income_needed),
                "passive_income": float(annual_passive_income / 12)
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    async def _generate_insights(self, request: FireCalculationRequest, years_to_fire: int, 
                               monthly_savings: Decimal, user_id: str) -> List[str]:
        """Gerar insights usando OpenAI"""
        
        try:
            # Dados para análise
            savings_rate = (monthly_savings / request.monthly_income) * 100
            current_age = request.current_age
            fire_age = current_age + years_to_fire
            
            prompt = f"""
            Analise a situação financeira FIRE de um brasileiro e forneça insights:
            
            Situação atual:
            - Idade: {current_age} anos
            - Renda mensal: R$ {request.monthly_income:,.2f}
            - Gastos mensais: R$ {request.monthly_expenses:,.2f}
            - Patrimônio atual: R$ {request.current_savings:,.2f}
            - Poupança mensal necessária: R$ {monthly_savings:,.2f}
            - Taxa de poupança: {savings_rate:.1f}%
            - Anos para FIRE: {years_to_fire}
            - Idade FIRE: {fire_age}
            
            Forneça 3-5 insights específicos e práticos para a realidade brasileira.
            Foque em ações concretas e estratégias otimizadas.
            """
            
            response = await self.openai_client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": """Você é um consultor financeiro especializado em FIRE no Brasil. 
                        Forneça insights práticos, específicos e acionáveis. 
                        Considere a realidade brasileira: impostos, inflação, tipos de investimento disponíveis."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            content = response.choices[0].message.content
            insights = [insight.strip() for insight in content.split('\n') if insight.strip() and not insight.strip().startswith('#')]
            
            return insights[:5]  # Máximo 5 insights
            
        except Exception as e:
            logger.error(f"Erro ao gerar insights: {str(e)}")
            return self._generate_fallback_insights(request, years_to_fire, monthly_savings)
    
    def _generate_fallback_insights(self, request: FireCalculationRequest, years_to_fire: int, 
                                  monthly_savings: Decimal) -> List[str]:
        """Insights de fallback baseados em regras"""
        
        insights = []
        savings_rate = (monthly_savings / request.monthly_income) * 100
        
        if savings_rate > 50:
            insights.append("Excelente! Sua taxa de poupança alta acelera significativamente o FIRE.")
        elif savings_rate > 30:
            insights.append("Boa taxa de poupança. Considere otimizar gastos para acelerar o processo.")
        else:
            insights.append("Taxa de poupança baixa. Foque em reduzir gastos ou aumentar renda.")
        
        if years_to_fire > 20:
            insights.append("Prazo longo para FIRE. Considere estratégias mais agressivas de economia.")
        elif years_to_fire < 10:
            insights.append("Prazo curto para FIRE! Você está no caminho certo.")
        
        if request.current_age > 35:
            insights.append("Começar FIRE após os 35 requer estratégias mais focadas. Priorize investimentos de maior retorno.")
        
        insights.append("Diversifique entre Tesouro Direto, ações e fundos imobiliários para otimizar retornos.")
        
        return insights
    
    def _generate_warnings(self, request: FireCalculationRequest, years_to_fire: int, 
                          monthly_savings: Decimal) -> List[str]:
        """Gerar alertas e considerações"""
        
        warnings = []
        savings_rate = (monthly_savings / request.monthly_income) * 100
        
        if savings_rate > 70:
            warnings.append("Taxa de poupança muito alta pode impactar qualidade de vida atual.")
        
        if years_to_fire > 30:
            warnings.append("Prazo muito longo. Considere revisar estratégias ou metas.")
        
        if request.current_age + years_to_fire > 65:
            warnings.append("FIRE após idade tradicional de aposentadoria. Considere previdência complementar.")
        
        if monthly_savings > request.monthly_income * Decimal('0.8'):
            warnings.append("Poupança necessária muito alta. Considere aumentar renda ou reduzir metas.")
        
        warnings.append("Considere inflação e mudanças na vida ao planejar FIRE.")
        warnings.append("Mantenha reserva de emergência separada do cálculo FIRE.")
        
        return warnings
    
    async def get_default_scenarios(self, user_id: str) -> Dict[str, Any]:
        """Obter cenários FIRE padrão"""
        
        return {
            "scenarios": {
                "lean_fire": {
                    "name": "Lean FIRE",
                    "description": "Vida simples com gastos reduzidos",
                    "monthly_target": 3000,
                    "fire_number": 900000,
                    "lifestyle": "Minimalista"
                },
                "regular_fire": {
                    "name": "Regular FIRE",
                    "description": "Vida confortável sem luxos",
                    "monthly_target": 6000,
                    "fire_number": 1800000,
                    "lifestyle": "Padrão"
                },
                "fat_fire": {
                    "name": "Fat FIRE",
                    "description": "Vida luxuosa sem restrições",
                    "monthly_target": 15000,
                    "fire_number": 4500000,
                    "lifestyle": "Luxo"
                }
            },
            "investment_profiles": {
                "conservador": {
                    "name": "Conservador",
                    "expected_return": 0.08,
                    "risk": "Baixo",
                    "allocation": "70% Renda Fixa, 30% Renda Variável"
                },
                "moderado": {
                    "name": "Moderado",
                    "expected_return": 0.10,
                    "risk": "Médio",
                    "allocation": "50% Renda Fixa, 50% Renda Variável"
                },
                "agressivo": {
                    "name": "Agressivo",
                    "expected_return": 0.12,
                    "risk": "Alto",
                    "allocation": "30% Renda Fixa, 70% Renda Variável"
                }
            }
        }
    
    def get_brazilian_investment_types(self) -> Dict[str, Any]:
        """Obter tipos de investimento brasileiros"""
        return self.investment_types