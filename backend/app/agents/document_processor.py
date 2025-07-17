"""
Agente de Processamento de Documentos
Responsável por extrair dados de documentos financeiros usando OCR e IA
"""

import asyncio
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

import cv2
import numpy as np
from PIL import Image
import pytesseract
import pdfplumber
import pandas as pd
from openai import AsyncOpenAI

from app.core.config import settings
from app.schemas.expense import ExpenseCreate
from app.utils.file_processing import FileProcessor

logger = logging.getLogger(__name__)

class DocumentProcessorAgent:
    """Agente para processamento de documentos financeiros"""
    
    def __init__(self):
        self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.file_processor = FileProcessor()
    
    async def process_document(self, file_path: str, user_id: str) -> Dict[str, Any]:
        """
        Processar documento financeiro e extrair dados
        
        Args:
            file_path: Caminho do arquivo
            user_id: ID do usuário
            
        Returns:
            Dict com dados extraídos e processados
        """
        try:
            # Determinar tipo de arquivo
            file_extension = os.path.splitext(file_path)[1].lower()
            
            if file_extension == '.pdf':
                extracted_data = await self._process_pdf(file_path)
            elif file_extension in ['.xlsx', '.xls']:
                extracted_data = await self._process_excel(file_path)
            elif file_extension == '.csv':
                extracted_data = await self._process_csv(file_path)
            elif file_extension in ['.jpg', '.jpeg', '.png']:
                extracted_data = await self._process_image(file_path)
            else:
                raise ValueError(f"Tipo de arquivo não suportado: {file_extension}")
            
            # Processar dados extraídos com OpenAI
            processed_data = await self._process_with_ai(extracted_data, user_id)
            
            return {
                "success": True,
                "file_type": file_extension,
                "raw_data": extracted_data,
                "processed_data": processed_data,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Erro ao processar documento: {str(e)}")
            raise
    
    async def _process_pdf(self, file_path: str) -> Dict[str, Any]:
        """Processar arquivo PDF"""
        try:
            text_content = ""
            tables = []
            
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    # Extrair texto
                    if page.extract_text():
                        text_content += page.extract_text() + "\n"
                    
                    # Extrair tabelas
                    page_tables = page.extract_tables()
                    if page_tables:
                        tables.extend(page_tables)
            
            return {
                "text": text_content,
                "tables": tables,
                "type": "pdf"
            }
            
        except Exception as e:
            logger.error(f"Erro ao processar PDF: {str(e)}")
            raise
    
    async def _process_excel(self, file_path: str) -> Dict[str, Any]:
        """Processar arquivo Excel"""
        try:
            # Ler todas as abas
            excel_data = pd.read_excel(file_path, sheet_name=None)
            
            processed_sheets = {}
            for sheet_name, df in excel_data.items():
                # Converter para formato processável
                processed_sheets[sheet_name] = {
                    "headers": df.columns.tolist(),
                    "data": df.to_dict('records'),
                    "shape": df.shape
                }
            
            return {
                "sheets": processed_sheets,
                "type": "excel"
            }
            
        except Exception as e:
            logger.error(f"Erro ao processar Excel: {str(e)}")
            raise
    
    async def _process_csv(self, file_path: str) -> Dict[str, Any]:
        """Processar arquivo CSV"""
        try:
            # Tentar diferentes encodings
            encodings = ['utf-8', 'latin1', 'cp1252', 'iso-8859-1']
            
            for encoding in encodings:
                try:
                    df = pd.read_csv(file_path, encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            else:
                raise ValueError("Não foi possível decodificar o arquivo CSV")
            
            return {
                "headers": df.columns.tolist(),
                "data": df.to_dict('records'),
                "shape": df.shape,
                "type": "csv"
            }
            
        except Exception as e:
            logger.error(f"Erro ao processar CSV: {str(e)}")
            raise
    
    async def _process_image(self, file_path: str) -> Dict[str, Any]:
        """Processar imagem usando OCR"""
        try:
            # Abrir e preprocessar imagem
            image = cv2.imread(file_path)
            
            # Converter para escala de cinza
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Aplicar threshold para melhorar OCR
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Extrair texto com Tesseract
            text = pytesseract.image_to_string(thresh, lang='por')
            
            # Obter dados estruturados
            data = pytesseract.image_to_data(thresh, lang='por', output_type=pytesseract.Output.DICT)
            
            return {
                "text": text,
                "ocr_data": data,
                "type": "image"
            }
            
        except Exception as e:
            logger.error(f"Erro ao processar imagem: {str(e)}")
            raise
    
    async def _process_with_ai(self, raw_data: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """
        Processar dados extraídos com OpenAI para identificar transações
        """
        try:
            # Criar prompt para OpenAI
            prompt = self._create_extraction_prompt(raw_data)
            
            response = await self.openai_client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": """Você é um assistente financeiro especializado em extrair dados de documentos financeiros brasileiros. 
                        Analise o conteúdo fornecido e extraia informações sobre transações financeiras.
                        
                        Retorne um JSON estruturado com:
                        - transactions: lista de transações encontradas
                        - summary: resumo do documento
                        - document_type: tipo do documento identificado
                        
                        Para cada transação, inclua:
                        - date: data da transação (formato YYYY-MM-DD)
                        - description: descrição da transação
                        - amount: valor (apenas números, sem símbolos)
                        - type: "expense" ou "income"
                        - category: categoria sugerida
                        - confidence: nível de confiança (0-1)
                        """
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=settings.OPENAI_TEMPERATURE,
                response_format={"type": "json_object"}
            )
            
            # Processar resposta
            ai_response = response.choices[0].message.content
            processed_data = eval(ai_response)  # Converter JSON string para dict
            
            return processed_data
            
        except Exception as e:
            logger.error(f"Erro ao processar com OpenAI: {str(e)}")
            raise
    
    def _create_extraction_prompt(self, raw_data: Dict[str, Any]) -> str:
        """Criar prompt para extração de dados"""
        
        data_type = raw_data.get("type", "unknown")
        
        if data_type == "pdf":
            content = f"Texto do PDF:\n{raw_data.get('text', '')}\n\n"
            if raw_data.get('tables'):
                content += f"Tabelas encontradas:\n{raw_data['tables']}\n"
        
        elif data_type == "excel":
            content = "Dados do Excel:\n"
            for sheet_name, sheet_data in raw_data.get('sheets', {}).items():
                content += f"\nPlanilha '{sheet_name}':\n"
                content += f"Colunas: {sheet_data['headers']}\n"
                content += f"Dados: {sheet_data['data'][:10]}\n"  # Primeiras 10 linhas
        
        elif data_type == "csv":
            content = f"Dados do CSV:\n"
            content += f"Colunas: {raw_data.get('headers', [])}\n"
            content += f"Dados: {raw_data.get('data', [])[:10]}\n"  # Primeiras 10 linhas
        
        elif data_type == "image":
            content = f"Texto extraído da imagem:\n{raw_data.get('text', '')}\n"
        
        else:
            content = f"Dados não estruturados:\n{raw_data}\n"
        
        return f"""
        Analise o seguinte conteúdo de um documento financeiro brasileiro:
        
        {content}
        
        Identifique e extraia todas as transações financeiras (receitas e despesas) que conseguir encontrar.
        Seja especialmente atento a:
        - Datas (formatos dd/mm/yyyy, dd/mm/yy, etc.)
        - Valores em reais (R$, BRL, etc.)
        - Descrições de estabelecimentos ou serviços
        - Categorias de gastos típicas brasileiras
        
        Retorne apenas um JSON válido com a estrutura solicitada.
        """
    
    def get_supported_formats(self) -> List[str]:
        """Obter formatos suportados"""
        return [".pdf", ".xlsx", ".xls", ".csv", ".jpg", ".jpeg", ".png"]
    
    async def validate_document(self, file_path: str) -> Dict[str, Any]:
        """Validar documento antes do processamento"""
        try:
            file_size = os.path.getsize(file_path)
            file_extension = os.path.splitext(file_path)[1].lower()
            
            return {
                "valid": file_extension in self.get_supported_formats(),
                "size": file_size,
                "max_size": settings.MAX_UPLOAD_SIZE,
                "size_valid": file_size <= settings.MAX_UPLOAD_SIZE,
                "extension": file_extension,
                "supported_formats": self.get_supported_formats()
            }
            
        except Exception as e:
            logger.error(f"Erro ao validar documento: {str(e)}")
            return {"valid": False, "error": str(e)}