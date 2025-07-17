"""
Agente Consultor Financeiro
Responsável por gerar insights, relatórios e recomendações financeiras
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, date, timedelta
from decimal import Decimal
from statistics import mean, median

from openai import AsyncOpenAI

from app.core.config import settings
from app.schemas.expense import ExpenseResponse, ExpenseStats
from app.schemas.fire import FireCalculationRequest

logger = logging.getLogger(__name__)

class FinancialAdvisorAgent:
    """Agente consultor financeiro para insights e recomendações"""
    
    def __init__(self):
        self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def generate_dashboard(self, user_id: str) -> Dict[str, Any]:
        """
        Gerar dados para dashboard principal
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Dados do dashboard
        """
        try:
            # TODO: Integrar com banco de dados real
            # Por enquanto, dados simulados
            mock_expenses = self._get_mock_expenses(user_id)
            
            # Calcular métricas principais
            current_month_expenses = self._calculate_current_month_expenses(mock_expenses)
            expense_trend = self._calculate_expense_trend(mock_expenses)
            category_breakdown = self._calculate_category_breakdown(mock_expenses)
            
            # Métricas FIRE
            fire_metrics = self._calculate_fire_metrics(user_id, current_month_expenses)
            
            # Insights rápidos
            quick_insights = await self._generate_quick_insights(
                current_month_expenses, expense_trend, category_breakdown, user_id
            )
            
            dashboard = {
                "overview": {
                    "current_month_expenses": current_month_expenses,
                    "expense_trend": expense_trend,
                    "savings_rate": fire_metrics.get("savings_rate", 0),
                    "fire_progress": fire_metrics.get("progress", 0)
                },
                "category_breakdown": category_breakdown,
                "fire_metrics": fire_metrics,
                "quick_insights": quick_insights,
                "last_updated": datetime.now().isoformat()
            }
            
            return dashboard
            
        except Exception as e:
            logger.error(f"Erro ao gerar dashboard: {str(e)}")
            raise
    
    async def generate_insights(self, user_id: str) -> Dict[str, Any]:
        """
        Gerar insights financeiros detalhados
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Insights detalhados
        """
        try:
            # Obter dados do usuário
            mock_expenses = self._get_mock_expenses(user_id)
            expense_stats = self._calculate_comprehensive_stats(mock_expenses)
            
            # Gerar insights com IA
            ai_insights = await self._generate_ai_insights(expense_stats, user_id)
            
            # Análise de padrões
            pattern_analysis = self._analyze_spending_patterns(mock_expenses)
            
            # Oportunidades de economia
            savings_opportunities = self._identify_savings_opportunities(mock_expenses)
            
            # Recomendações de investimento
            investment_recommendations = await self._generate_investment_recommendations(
                expense_stats, user_id
            )
            
            insights = {
                "ai_insights": ai_insights,
                "pattern_analysis": pattern_analysis,
                "savings_opportunities": savings_opportunities,
                "investment_recommendations": investment_recommendations,
                "expense_stats": expense_stats,
                "generated_at": datetime.now().isoformat()
            }
            
            return insights
            
        except Exception as e:
            logger.error(f"Erro ao gerar insights: {str(e)}")
            raise
    
    async def generate_monthly_report(self, user_id: str, month: Optional[str] = None) -> Dict[str, Any]:
        """
        Gerar relatório mensal detalhado
        
        Args:
            user_id: ID do usuário
            month: Mês específico (formato YYYY-MM)
            
        Returns:
            Relatório mensal
        """
        try:
            # Definir período
            if month:
                report_date = datetime.strptime(month, "%Y-%m")
            else:
                report_date = datetime.now().replace(day=1)
            
            # Obter dados do mês
            mock_expenses = self._get_mock_expenses_for_month(user_id, report_date)
            
            # Calcular métricas do mês
            monthly_stats = self._calculate_monthly_stats(mock_expenses, report_date)
            
            # Comparar com mês anterior
            comparison = self._compare_with_previous_month(user_id, report_date)
            
            # Gerar análise com IA
            monthly_analysis = await self._generate_monthly_analysis(
                monthly_stats, comparison, user_id
            )
            
            # Metas do mês
            monthly_goals = self._evaluate_monthly_goals(monthly_stats, user_id)
            
            # Projeções para próximo mês
            next_month_projections = self._project_next_month(mock_expenses, monthly_stats)
            
            report = {
                "period": {
                    "month": report_date.strftime("%Y-%m"),
                    "month_name": report_date.strftime("%B %Y"),
                    "days_in_month": (report_date.replace(month=report_date.month + 1, day=1) - timedelta(days=1)).day
                },
                "monthly_stats": monthly_stats,
                "comparison": comparison,
                "analysis": monthly_analysis,
                "goals": monthly_goals,
                "projections": next_month_projections,
                "generated_at": datetime.now().isoformat()
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Erro ao gerar relatório mensal: {str(e)}")
            raise
    
    def _get_mock_expenses(self, user_id: str) -> List[Dict[str, Any]]:
        """Gerar dados mock de despesas para desenvolvimento"""
        
        # Dados simulados para desenvolvimento
        mock_expenses = [
            {
                "date": "2024-01-15",
                "description": "Supermercado Pão de Açúcar",
                "amount": 250.00,
                "category": "alimentacao",
                "subcategory": "supermercado"
            },
            {
                "date": "2024-01-16",
                "description": "Posto Shell",
                "amount": 80.00,
                "category": "transporte",
                "subcategory": "combustivel"
            },
            {
                "date": "2024-01-17",
                "description": "Restaurante Outback",
                "amount": 120.00,
                "category": "alimentacao",
                "subcategory": "restaurante"
            },
            {
                "date": "2024-01-18",
                "description": "Uber",
                "amount": 25.00,
                "category": "transporte",
                "subcategory": "uber"
            },
            {
                "date": "2024-01-19",
                "description": "Farmácia Droga Raia",
                "amount": 45.00,
                "category": "saude",
                "subcategory": "farmacia"
            }
        ]
        
        return mock_expenses
    
    def _get_mock_expenses_for_month(self, user_id: str, month: datetime) -> List[Dict[str, Any]]:
        """Obter despesas mock para mês específico"""
        
        # Simular dados do mês
        return self._get_mock_expenses(user_id)
    
    def _calculate_current_month_expenses(self, expenses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calcular gastos do mês atual"""
        
        total = sum(expense["amount"] for expense in expenses)
        count = len(expenses)
        average = total / count if count > 0 else 0
        
        return {
            "total": total,
            "count": count,
            "average": average,
            "currency": "BRL"
        }
    
    def _calculate_expense_trend(self, expenses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calcular tendência de gastos"""
        
        # Simulação de tendência
        return {
            "direction": "increasing",
            "percentage": 5.2,
            "description": "Gastos aumentaram 5.2% em relação ao mês anterior"
        }
    
    def _calculate_category_breakdown(self, expenses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calcular breakdown por categoria"""
        
        category_totals = {}
        total_amount = sum(expense["amount"] for expense in expenses)
        
        for expense in expenses:
            category = expense["category"]
            if category not in category_totals:
                category_totals[category] = 0
            category_totals[category] += expense["amount"]
        
        # Calcular percentuais
        breakdown = {}
        for category, amount in category_totals.items():
            percentage = (amount / total_amount) * 100 if total_amount > 0 else 0
            breakdown[category] = {
                "amount": amount,
                "percentage": round(percentage, 1),
                "currency": "BRL"
            }
        
        return breakdown
    
    def _calculate_fire_metrics(self, user_id: str, current_expenses: Dict[str, Any]) -> Dict[str, Any]:
        """Calcular métricas FIRE simuladas"""
        
        # Dados simulados
        monthly_income = 8000
        monthly_expenses = current_expenses["total"]
        monthly_savings = monthly_income - monthly_expenses
        savings_rate = (monthly_savings / monthly_income) * 100
        
        # Simular progresso FIRE
        fire_number = monthly_expenses * 12 * 25  # Regra 25x
        current_net_worth = 50000  # Simulado
        fire_progress = (current_net_worth / fire_number) * 100
        
        return {
            "monthly_income": monthly_income,
            "monthly_expenses": monthly_expenses,
            "monthly_savings": monthly_savings,
            "savings_rate": round(savings_rate, 1),
            "fire_number": fire_number,
            "current_net_worth": current_net_worth,
            "progress": round(fire_progress, 1),
            "currency": "BRL"
        }
    
    async def _generate_quick_insights(self, current_expenses: Dict[str, Any], 
                                     trend: Dict[str, Any], breakdown: Dict[str, Any], 
                                     user_id: str) -> List[str]:
        """Gerar insights rápidos"""
        
        try:
            prompt = f"""
            Analise a situação financeira atual e forneça 3 insights rápidos:
            
            Gastos do mês: R$ {current_expenses['total']:,.2f}
            Tendência: {trend['description']}
            Principais categorias: {list(breakdown.keys())[:3]}
            
            Forneça insights práticos e acionáveis para um brasileiro.
            """
            
            response = await self.openai_client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um consultor financeiro brasileiro. Forneça insights curtos e práticos."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=200
            )
            
            content = response.choices[0].message.content
            insights = [insight.strip() for insight in content.split('\n') if insight.strip()]
            
            return insights[:3]
            
        except Exception as e:
            logger.error(f"Erro ao gerar insights rápidos: {str(e)}")
            return [
                "Monitore seus gastos com alimentação, geralmente a maior categoria",
                "Considere usar o PIX para evitar taxas bancárias",
                "Revise gastos mensais para identificar oportunidades de economia"
            ]
    
    def _calculate_comprehensive_stats(self, expenses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calcular estatísticas abrangentes"""
        
        if not expenses:
            return {"total": 0, "count": 0, "average": 0}
        
        amounts = [expense["amount"] for expense in expenses]
        
        return {
            "total": sum(amounts),
            "count": len(amounts),
            "average": mean(amounts),
            "median": median(amounts),
            "min": min(amounts),
            "max": max(amounts),
            "currency": "BRL"
        }
    
    async def _generate_ai_insights(self, stats: Dict[str, Any], user_id: str) -> List[str]:
        """Gerar insights com IA"""
        
        try:
            prompt = f"""
            Analise os dados financeiros e forneça insights específicos:
            
            Estatísticas:
            - Total gasto: R$ {stats['total']:,.2f}
            - Média por transação: R$ {stats['average']:,.2f}
            - Mediana: R$ {stats['median']:,.2f}
            - Número de transações: {stats['count']}
            
            Forneça 5 insights práticos para otimização financeira no Brasil.
            """
            
            response = await self.openai_client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um especialista em finanças pessoais brasileiras. Forneça insights acionáveis."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=400
            )
            
            content = response.choices[0].message.content
            insights = [insight.strip() for insight in content.split('\n') if insight.strip()]
            
            return insights[:5]
            
        except Exception as e:
            logger.error(f"Erro ao gerar insights AI: {str(e)}")
            return ["Análise de insights temporariamente indisponível"]
    
    def _analyze_spending_patterns(self, expenses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analisar padrões de gastos"""
        
        # Análise por categoria
        category_patterns = {}
        for expense in expenses:
            category = expense["category"]
            if category not in category_patterns:
                category_patterns[category] = []
            category_patterns[category].append(expense["amount"])
        
        patterns = {}
        for category, amounts in category_patterns.items():
            patterns[category] = {
                "frequency": len(amounts),
                "average": mean(amounts),
                "total": sum(amounts),
                "pattern": "regular" if len(amounts) > 2 else "occasional"
            }
        
        return {
            "category_patterns": patterns,
            "most_frequent_category": max(patterns.keys(), key=lambda x: patterns[x]["frequency"]),
            "highest_spending_category": max(patterns.keys(), key=lambda x: patterns[x]["total"])
        }
    
    def _identify_savings_opportunities(self, expenses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identificar oportunidades de economia"""
        
        opportunities = []
        
        # Análise por categoria
        category_totals = {}
        for expense in expenses:
            category = expense["category"]
            if category not in category_totals:
                category_totals[category] = 0
            category_totals[category] += expense["amount"]
        
        # Identificar categorias com maior potencial
        for category, total in category_totals.items():
            if total > 200:  # Limiar para sugestão
                opportunities.append({
                    "category": category,
                    "current_spending": total,
                    "potential_savings": total * 0.1,  # 10% de economia
                    "recommendation": f"Considere revisar gastos em {category}",
                    "difficulty": "easy"
                })
        
        return opportunities
    
    async def _generate_investment_recommendations(self, stats: Dict[str, Any], user_id: str) -> List[Dict[str, Any]]:
        """Gerar recomendações de investimento"""
        
        recommendations = [
            {
                "type": "Tesouro Direto",
                "allocation": 40,
                "risk": "Baixo",
                "expected_return": 8.5,
                "description": "Base segura para carteira conservadora"
            },
            {
                "type": "Fundos Imobiliários",
                "allocation": 30,
                "risk": "Médio",
                "expected_return": 10.0,
                "description": "Renda passiva através de imóveis"
            },
            {
                "type": "Ações",
                "allocation": 30,
                "risk": "Alto",
                "expected_return": 12.0,
                "description": "Crescimento de longo prazo"
            }
        ]
        
        return recommendations
    
    def _calculate_monthly_stats(self, expenses: List[Dict[str, Any]], month: datetime) -> Dict[str, Any]:
        """Calcular estatísticas mensais"""
        
        return self._calculate_comprehensive_stats(expenses)
    
    def _compare_with_previous_month(self, user_id: str, current_month: datetime) -> Dict[str, Any]:
        """Comparar com mês anterior"""
        
        # Simulado
        return {
            "previous_month_total": 4800,
            "current_month_total": 5200,
            "change_amount": 400,
            "change_percentage": 8.3,
            "trend": "increase"
        }
    
    async def _generate_monthly_analysis(self, stats: Dict[str, Any], 
                                       comparison: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """Gerar análise mensal"""
        
        return {
            "summary": f"Gastos do mês: R$ {stats['total']:,.2f}",
            "highlights": [
                "Gastos aumentaram em relação ao mês anterior",
                "Categoria alimentação representa maior parte",
                "Oportunidade de economia em transporte"
            ],
            "recommendations": [
                "Definir orçamento mensal por categoria",
                "Revisar gastos com alimentação",
                "Considerar alternativas de transporte"
            ]
        }
    
    def _evaluate_monthly_goals(self, stats: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """Avaliar metas mensais"""
        
        return {
            "budget_goal": 5000,
            "actual_spending": stats["total"],
            "goal_achieved": stats["total"] <= 5000,
            "variance": stats["total"] - 5000,
            "performance": "on_track" if stats["total"] <= 5000 else "over_budget"
        }
    
    def _project_next_month(self, expenses: List[Dict[str, Any]], 
                           current_stats: Dict[str, Any]) -> Dict[str, Any]:
        """Projetar próximo mês"""
        
        # Projeção simples baseada na média
        projected_total = current_stats["average"] * 1.05  # 5% de crescimento
        
        return {
            "projected_total": projected_total,
            "confidence": 0.75,
            "basis": "Baseado em padrões históricos",
            "recommendations": [
                "Estabelecer orçamento mensal",
                "Monitorar gastos semanalmente"
            ]
        }