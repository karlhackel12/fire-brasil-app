"""
Gerenciador MCP (Model Context Protocol) para FIRE Brasil
Adaptação do sistema MCP para nossa aplicação
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from app.core.config import settings

logger = logging.getLogger(__name__)

@dataclass
class MCPServer:
    """Configuração de um servidor MCP"""
    name: str
    command: str
    args: List[str]
    env: Dict[str, str] = None
    process: Optional[asyncio.subprocess.Process] = None
    status: str = "stopped"

class MCPManager:
    """Gerenciador de servidores MCP"""
    
    def __init__(self):
        self.servers: Dict[str, MCPServer] = {}
        self.initialized = False
    
    async def initialize(self):
        """Inicializar todos os servidores MCP"""
        try:
            logger.info("Inicializando gerenciador MCP...")
            
            # Configurar servidores baseados no settings
            for name, config in settings.MCP_SERVERS.items():
                server = MCPServer(
                    name=name,
                    command=config["command"],
                    args=config["args"],
                    env=config.get("env", {})
                )
                self.servers[name] = server
            
            # Iniciar servidores críticos
            await self._start_core_servers()
            
            self.initialized = True
            logger.info("Gerenciador MCP inicializado com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao inicializar MCP: {str(e)}")
            raise
    
    async def _start_core_servers(self):
        """Iniciar servidores essenciais"""
        core_servers = [
            "document_processor",
            "expense_categorizer", 
            "fire_calculator",
            "financial_advisor"
        ]
        
        for server_name in core_servers:
            if server_name in self.servers:
                await self.start_server(server_name)
    
    async def start_server(self, server_name: str) -> bool:
        """Iniciar servidor MCP específico"""
        try:
            if server_name not in self.servers:
                logger.error(f"Servidor {server_name} não encontrado")
                return False
            
            server = self.servers[server_name]
            
            # Verificar se já está rodando
            if server.process and server.process.returncode is None:
                logger.info(f"Servidor {server_name} já está rodando")
                return True
            
            # Iniciar processo
            logger.info(f"Iniciando servidor {server_name}...")
            
            # Para nosso caso simplificado, não vamos iniciar processos separados
            # Vamos simular o comportamento MCP dentro da aplicação
            server.status = "running"
            server.process = None  # Placeholder
            
            logger.info(f"Servidor {server_name} iniciado com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao iniciar servidor {server_name}: {str(e)}")
            return False
    
    async def stop_server(self, server_name: str) -> bool:
        """Parar servidor MCP específico"""
        try:
            if server_name not in self.servers:
                return False
            
            server = self.servers[server_name]
            
            if server.process:
                server.process.terminate()
                await server.process.wait()
            
            server.status = "stopped"
            server.process = None
            
            logger.info(f"Servidor {server_name} parado")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao parar servidor {server_name}: {str(e)}")
            return False
    
    async def call_server(self, server_name: str, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Chamar método em servidor MCP"""
        try:
            if server_name not in self.servers:
                raise ValueError(f"Servidor {server_name} não encontrado")
            
            server = self.servers[server_name]
            
            if server.status != "running":
                raise ValueError(f"Servidor {server_name} não está rodando")
            
            # Para nossa implementação simplificada, vamos rotear chamadas
            # diretamente para os agentes correspondentes
            return await self._route_call(server_name, method, params)
            
        except Exception as e:
            logger.error(f"Erro ao chamar {server_name}.{method}: {str(e)}")
            raise
    
    async def _route_call(self, server_name: str, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Rotear chamada para agente apropriado"""
        
        # Importar agentes dinamicamente para evitar imports circulares
        if server_name == "document_processor":
            from app.agents.document_processor import DocumentProcessorAgent
            agent = DocumentProcessorAgent()
            
            if method == "process_document":
                return await agent.process_document(
                    params.get("file_path"),
                    params.get("user_id")
                )
            elif method == "validate_document":
                return await agent.validate_document(params.get("file_path"))
        
        elif server_name == "expense_categorizer":
            from app.agents.expense_categorizer import ExpenseCategorizerAgent
            agent = ExpenseCategorizerAgent()
            
            if method == "categorize_batch":
                return await agent.categorize_batch(
                    params.get("expenses"),
                    params.get("user_id")
                )
            elif method == "categorize_single":
                return await agent.categorize_single(
                    params.get("expense"),
                    params.get("user_id")
                )
        
        elif server_name == "fire_calculator":
            from app.agents.fire_calculator import FireCalculatorAgent
            agent = FireCalculatorAgent()
            
            if method == "calculate_fire_projections":
                return await agent.calculate_fire_projections(
                    params.get("request"),
                    params.get("user_id")
                )
        
        elif server_name == "financial_advisor":
            from app.agents.financial_advisor import FinancialAdvisorAgent
            agent = FinancialAdvisorAgent()
            
            if method == "generate_dashboard":
                return await agent.generate_dashboard(params.get("user_id"))
            elif method == "generate_insights":
                return await agent.generate_insights(params.get("user_id"))
        
        raise ValueError(f"Método {method} não encontrado em {server_name}")
    
    async def get_status(self) -> Dict[str, Any]:
        """Obter status de todos os servidores"""
        status = {
            "initialized": self.initialized,
            "servers": {}
        }
        
        for name, server in self.servers.items():
            status["servers"][name] = {
                "name": name,
                "status": server.status,
                "command": server.command,
                "args": server.args
            }
        
        return status
    
    async def restart_server(self, server_name: str) -> bool:
        """Reiniciar servidor MCP"""
        try:
            await self.stop_server(server_name)
            await asyncio.sleep(1)  # Aguardar um pouco
            return await self.start_server(server_name)
            
        except Exception as e:
            logger.error(f"Erro ao reiniciar servidor {server_name}: {str(e)}")
            return False
    
    async def cleanup(self):
        """Limpeza na finalização"""
        try:
            logger.info("Finalizando gerenciador MCP...")
            
            # Parar todos os servidores
            for server_name in self.servers:
                await self.stop_server(server_name)
            
            self.initialized = False
            logger.info("Gerenciador MCP finalizado")
            
        except Exception as e:
            logger.error(f"Erro na limpeza MCP: {str(e)}")
    
    def get_server_names(self) -> List[str]:
        """Obter nomes de todos os servidores"""
        return list(self.servers.keys())
    
    def is_server_running(self, server_name: str) -> bool:
        """Verificar se servidor está rodando"""
        if server_name not in self.servers:
            return False
        return self.servers[server_name].status == "running"