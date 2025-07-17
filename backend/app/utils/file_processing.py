"""
Utilitários para processamento de arquivos
"""

import os
import magic
import hashlib
from typing import Dict, Any, List, Optional
from pathlib import Path

class FileProcessor:
    """Processador de arquivos com validações e metadados"""
    
    def __init__(self):
        self.supported_extensions = {
            '.pdf': 'application/pdf',
            '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            '.xls': 'application/vnd.ms-excel',
            '.csv': 'text/csv',
            '.txt': 'text/plain',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png'
        }
    
    def validate_file(self, file_path: str) -> Dict[str, Any]:
        """Validar arquivo"""
        
        if not os.path.exists(file_path):
            return {"valid": False, "error": "Arquivo não encontrado"}
        
        # Verificar extensão
        file_extension = Path(file_path).suffix.lower()
        if file_extension not in self.supported_extensions:
            return {
                "valid": False,
                "error": f"Extensão {file_extension} não suportada"
            }
        
        # Verificar tamanho
        file_size = os.path.getsize(file_path)
        max_size = 10 * 1024 * 1024  # 10MB
        
        if file_size > max_size:
            return {
                "valid": False,
                "error": f"Arquivo muito grande ({file_size} bytes)"
            }
        
        # Verificar tipo MIME
        try:
            mime_type = magic.from_file(file_path, mime=True)
            expected_mime = self.supported_extensions[file_extension]
            
            if mime_type != expected_mime:
                return {
                    "valid": False,
                    "error": f"Tipo MIME inválido: {mime_type}"
                }
        except:
            # Se magic não funcionar, pular verificação MIME
            pass
        
        return {"valid": True, "size": file_size, "extension": file_extension}
    
    def get_file_metadata(self, file_path: str) -> Dict[str, Any]:
        """Obter metadados do arquivo"""
        
        stat = os.stat(file_path)
        
        return {
            "name": os.path.basename(file_path),
            "size": stat.st_size,
            "extension": Path(file_path).suffix.lower(),
            "created": stat.st_ctime,
            "modified": stat.st_mtime,
            "hash": self._calculate_hash(file_path)
        }
    
    def _calculate_hash(self, file_path: str) -> str:
        """Calcular hash MD5 do arquivo"""
        
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def is_supported_format(self, file_path: str) -> bool:
        """Verificar se formato é suportado"""
        
        extension = Path(file_path).suffix.lower()
        return extension in self.supported_extensions
    
    def get_supported_formats(self) -> List[str]:
        """Obter formatos suportados"""
        
        return list(self.supported_extensions.keys())