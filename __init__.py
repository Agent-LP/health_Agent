"""
Sistema RAG de Consejos de Salud
"""

__version__ = "1.0.0"

from .rag_system import HealthRAGSystem
from .document_loader import load_all_documents, split_documents

__all__ = [
    "HealthRAGSystem",
    "load_all_documents",
    "split_documents",
]





