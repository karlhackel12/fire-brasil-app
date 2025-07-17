"""
Agente de Categorização de Despesas
Responsável por classificar gastos automaticamente usando OpenAI
"""

import asyncio
import json
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import re

from openai import AsyncOpenAI

from app.core.config import settings, BRAZILIAN_EXPENSE_CATEGORIES
from app.schemas.expense import ExpenseCreate, ExpenseResponse, ExpenseCategory

logger = logging.getLogger(__name__)

class ExpenseCategorizerAgent:
    """Agente para categorização automática de despesas"""
    
    def __init__(self):
        self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.categories = BRAZILIAN_EXPENSE_CATEGORIES
        self.learning_cache = {}  # Cache para aprendizado
    
    async def categorize_single(self, expense: ExpenseCreate, user_id: str) -> ExpenseResponse:
        """
        Categorizar uma única despesa
        
        Args:
            expense: Despesa para categorizar
            user_id: ID do usuário
            
        Returns:
            Despesa categorizada
        """
        try:
            # Categorizar usando OpenAI
            categorization = await self._categorize_with_ai(expense, user_id)
            
            # Criar response com dados da IA
            response = ExpenseResponse(
                id=0,  # Será definido quando salvar no banco
                user_id=user_id,
                created_at=datetime.now(),
                date=expense.date,
                description=expense.description,
                amount=expense.amount,
                type=expense.type,
                category=categorization["category"],
                subcategory=categorization["subcategory"],
                payment_method=expense.payment_method,
                tags=expense.tags or [],
                notes=expense.notes,
                ai_confidence=categorization["confidence"],
                ai_suggested_category=categorization["suggested_category"],
                ai_reasoning=categorization["reasoning"]
            )
            
            # Atualizar cache de aprendizado
            self._update_learning_cache(user_id, expense.description, categorization)
            
            return response
            
        except Exception as e:
            logger.error(f"Erro ao categorizar despesa: {str(e)}")
            raise
    
    async def categorize_batch(self, expenses: List[ExpenseCreate], user_id: str) -> List[ExpenseResponse]:
        """
        Categorizar múltiplas despesas em lote
        
        Args:
            expenses: Lista de despesas
            user_id: ID do usuário
            
        Returns:
            Lista de despesas categorizadas
        """
        try:
            # Processar em lotes menores para evitar timeout
            batch_size = 10
            results = []
            
            for i in range(0, len(expenses), batch_size):
                batch = expenses[i:i + batch_size]
                
                # Processar lote
                batch_results = await self._categorize_batch_with_ai(batch, user_id)
                results.extend(batch_results)
                
                # Aguardar um pouco entre lotes
                if i + batch_size < len(expenses):
                    await asyncio.sleep(0.5)
            
            return results
            
        except Exception as e:
            logger.error(f"Erro ao categorizar lote: {str(e)}")
            raise
    
    async def _categorize_with_ai(self, expense: ExpenseCreate, user_id: str) -> Dict[str, Any]:
        """Categorizar despesa única usando OpenAI"""
        
        # Verificar cache primeiro
        cached_result = self._check_cache(user_id, expense.description)
        if cached_result:
            return cached_result
        
        try:
            # Criar prompt para categorização
            prompt = self._create_categorization_prompt(expense, user_id)
            
            response = await self.openai_client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt()
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,  # Baixa criatividade para consistência
                response_format={"type": "json_object"}
            )
            
            # Processar resposta
            ai_response = json.loads(response.choices[0].message.content)
            
            # Validar e normalizar resposta
            categorization = self._validate_ai_response(ai_response)
            
            return categorization
            
        except Exception as e:
            logger.error(f"Erro na categorização AI: {str(e)}")
            # Fallback para categorização básica
            return self._fallback_categorization(expense)
    
    async def _categorize_batch_with_ai(self, expenses: List[ExpenseCreate], user_id: str) -> List[ExpenseResponse]:
        """Categorizar lote de despesas usando OpenAI"""
        
        try:
            # Criar prompt para lote
            prompt = self._create_batch_prompt(expenses, user_id)
            
            response = await self.openai_client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_batch_system_prompt()
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            
            # Processar resposta
            ai_response = json.loads(response.choices[0].message.content)
            
            # Criar objetos de resposta
            results = []
            for i, expense in enumerate(expenses):
                categorization = ai_response.get("categorizations", [{}])[i] if i < len(ai_response.get("categorizations", [])) else {}
                
                # Validar categorização
                validated_cat = self._validate_ai_response(categorization)
                
                # Criar response
                response_obj = ExpenseResponse(
                    id=0,
                    user_id=user_id,
                    created_at=datetime.now(),
                    date=expense.date,
                    description=expense.description,
                    amount=expense.amount,
                    type=expense.type,
                    category=validated_cat["category"],
                    subcategory=validated_cat["subcategory"],
                    payment_method=expense.payment_method,
                    tags=expense.tags or [],
                    notes=expense.notes,
                    ai_confidence=validated_cat["confidence"],
                    ai_suggested_category=validated_cat["suggested_category"],
                    ai_reasoning=validated_cat["reasoning"]
                )
                
                results.append(response_obj)
                
                # Atualizar cache
                self._update_learning_cache(user_id, expense.description, validated_cat)
            
            return results
            
        except Exception as e:
            logger.error(f"Erro na categorização em lote: {str(e)}")
            # Fallback para categorização individual
            return [await self.categorize_single(expense, user_id) for expense in expenses]
    
    def _get_system_prompt(self) -> str:
        """Obter prompt do sistema para categorização"""
        
        categories_text = ""
        for key, category in self.categories.items():
            categories_text += f"- {key}: {category['name']} {category['icon']}\n"
            categories_text += f"  Subcategorias: {', '.join(category['subcategories'])}\n"
        
        return f"""
        Você é um assistente financeiro brasileiro especializado em categorizar despesas pessoais.
        
        CATEGORIAS DISPONÍVEIS:
        {categories_text}
        
        INSTRUÇÕES:
        1. Analise a descrição da despesa
        2. Identifique padrões de estabelecimentos brasileiros
        3. Classifique na categoria mais apropriada
        4. Sugira uma subcategoria específica
        5. Avalie sua confiança (0-1)
        6. Explique brevemente seu raciocínio
        
        FORMATO DE RESPOSTA (JSON):
        {{
            "category": "categoria_principal",
            "subcategory": "subcategoria_especifica",
            "confidence": 0.95,
            "suggested_category": "categoria_sugerida",
            "reasoning": "explicação_breve"
        }}
        
        EXEMPLOS BRASILEIROS:
        - "Pão de Açúcar" → alimentacao/supermercado
        - "Uber" → transporte/uber
        - "Posto Ipiranga" → transporte/combustivel
        - "Farmácia Droga Raia" → saude/farmacia
        - "Cinema Cinemark" → lazer/cinema
        """
    
    def _get_batch_system_prompt(self) -> str:
        """Prompt para categorização em lote"""
        return self._get_system_prompt() + """
        
        FORMATO PARA LOTE:
        {
            "categorizations": [
                {
                    "category": "categoria1",
                    "subcategory": "sub1",
                    "confidence": 0.9,
                    "suggested_category": "sugestao1",
                    "reasoning": "explicacao1"
                },
                ...
            ]
        }
        """
    
    def _create_categorization_prompt(self, expense: ExpenseCreate, user_id: str) -> str:
        """Criar prompt para categorização individual"""
        
        user_history = self._get_user_history(user_id)
        
        return f"""
        Categorize a seguinte despesa:
        
        Data: {expense.date}
        Descrição: "{expense.description}"
        Valor: R$ {expense.amount}
        Tipo: {expense.type}
        
        {user_history}
        
        Retorne apenas um JSON válido com a categorização.
        """
    
    def _create_batch_prompt(self, expenses: List[ExpenseCreate], user_id: str) -> str:
        """Criar prompt para lote de despesas"""
        
        user_history = self._get_user_history(user_id)
        expenses_text = ""
        
        for i, expense in enumerate(expenses):
            expenses_text += f"{i+1}. {expense.date} - \"{expense.description}\" - R$ {expense.amount}\n"
        
        return f"""
        Categorize as seguintes despesas:
        
        {expenses_text}
        
        {user_history}
        
        Retorne um JSON com array de categorizações na mesma ordem.
        """
    
    def _validate_ai_response(self, ai_response: Dict[str, Any]) -> Dict[str, Any]:
        """Validar e normalizar resposta da IA"""
        
        # Valores padrão
        default_response = {
            "category": "outros",
            "subcategory": "diversos",
            "confidence": 0.5,
            "suggested_category": "outros",
            "reasoning": "Categorização automática"
        }
        
        if not ai_response:
            return default_response
        
        # Validar categoria
        category = ai_response.get("category", "outros")
        if category not in self.categories:
            category = "outros"
        
        # Validar subcategoria
        subcategory = ai_response.get("subcategory", "diversos")
        if subcategory not in self.categories[category]["subcategories"]:
            subcategory = self.categories[category]["subcategories"][0]
        
        # Validar confiança
        confidence = ai_response.get("confidence", 0.5)
        if not isinstance(confidence, (int, float)) or confidence < 0 or confidence > 1:
            confidence = 0.5
        
        return {
            "category": category,
            "subcategory": subcategory,
            "confidence": float(confidence),
            "suggested_category": ai_response.get("suggested_category", category),
            "reasoning": ai_response.get("reasoning", "Categorização automática")
        }
    
    def _fallback_categorization(self, expense: ExpenseCreate) -> Dict[str, Any]:
        """Categorização de fallback baseada em regras"""
        
        description = expense.description.lower()
        
        # Regras simples baseadas em palavras-chave
        if any(word in description for word in ["mercado", "supermercado", "padaria", "açougue"]):
            return {
                "category": "alimentacao",
                "subcategory": "supermercado",
                "confidence": 0.7,
                "suggested_category": "alimentacao",
                "reasoning": "Identificado por palavra-chave"
            }
        
        elif any(word in description for word in ["uber", "99", "taxi", "combustivel", "posto"]):
            return {
                "category": "transporte",
                "subcategory": "uber" if "uber" in description else "combustivel",
                "confidence": 0.8,
                "suggested_category": "transporte",
                "reasoning": "Identificado por palavra-chave"
            }
        
        elif any(word in description for word in ["farmacia", "droga", "medico", "hospital"]):
            return {
                "category": "saude",
                "subcategory": "farmacia",
                "confidence": 0.6,
                "suggested_category": "saude",
                "reasoning": "Identificado por palavra-chave"
            }
        
        # Padrão
        return {
            "category": "outros",
            "subcategory": "diversos",
            "confidence": 0.3,
            "suggested_category": "outros",
            "reasoning": "Não foi possível categorizar automaticamente"
        }
    
    def _check_cache(self, user_id: str, description: str) -> Optional[Dict[str, Any]]:
        """Verificar cache de aprendizado"""
        
        user_cache = self.learning_cache.get(user_id, {})
        
        # Buscar por descrição exata
        if description in user_cache:
            return user_cache[description]
        
        # Buscar por similaridade (implementação simples)
        for cached_desc, categorization in user_cache.items():
            if self._calculate_similarity(description, cached_desc) > 0.8:
                return categorization
        
        return None
    
    def _update_learning_cache(self, user_id: str, description: str, categorization: Dict[str, Any]):
        """Atualizar cache de aprendizado"""
        
        if user_id not in self.learning_cache:
            self.learning_cache[user_id] = {}
        
        self.learning_cache[user_id][description] = categorization
        
        # Limitar tamanho do cache
        if len(self.learning_cache[user_id]) > 1000:
            # Remove entradas mais antigas
            items = list(self.learning_cache[user_id].items())
            self.learning_cache[user_id] = dict(items[-500:])
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calcular similaridade entre textos (implementação simples)"""
        
        # Normalizar textos
        text1 = re.sub(r'[^\w\s]', '', text1.lower())
        text2 = re.sub(r'[^\w\s]', '', text2.lower())
        
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    def _get_user_history(self, user_id: str) -> str:
        """Obter histórico do usuário para contexto"""
        
        user_cache = self.learning_cache.get(user_id, {})
        
        if not user_cache:
            return ""
        
        # Pegar exemplos recentes
        recent_examples = list(user_cache.items())[-5:]
        
        history_text = "EXEMPLOS ANTERIORES DO USUÁRIO:\n"
        for description, categorization in recent_examples:
            history_text += f"- \"{description}\" → {categorization['category']}/{categorization['subcategory']}\n"
        
        return history_text
    
    def get_brazilian_categories(self) -> Dict[str, Any]:
        """Obter categorias brasileiras"""
        return self.categories
    
    def get_category_suggestions(self, description: str) -> List[Dict[str, Any]]:
        """Obter sugestões de categoria baseadas na descrição"""
        
        suggestions = []
        description_lower = description.lower()
        
        for category_key, category_info in self.categories.items():
            score = 0
            
            # Verificar nome da categoria
            if category_info["name"].lower() in description_lower:
                score += 0.8
            
            # Verificar subcategorias
            for subcategory in category_info["subcategories"]:
                if subcategory in description_lower:
                    score += 0.6
            
            if score > 0:
                suggestions.append({
                    "category": category_key,
                    "name": category_info["name"],
                    "icon": category_info["icon"],
                    "score": score
                })
        
        # Ordenar por score
        suggestions.sort(key=lambda x: x["score"], reverse=True)
        
        return suggestions[:3]  # Top 3 sugestões