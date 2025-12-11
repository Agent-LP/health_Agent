"""
Configuración del sistema RAG para consejos de salud
"""
import os
from pathlib import Path

# Rutas del proyecto
BASE_DIR = Path(__file__).parent
DOCS_DIR = BASE_DIR / "docs"
VECTORSTORE_DIR = BASE_DIR / "vectorstore"

# Configuración del modelo
LLM_MODEL = "gemma3:1b"  # Cambiar según el modelo disponible
LLM_TEMPERATURE = 0

# Configuración de embeddings
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Configuración de chunking
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Configuración de retriever
RETRIEVER_K = 15 # Número de documentos a recuperar por defecto
RETRIEVER_SCORE_THRESHOLD = 0.5  # Umbral mínimo de relevancia (opcional)

# Tipos de archivos soportados
SUPPORTED_FILE_TYPES = [".pdf", ".txt", ".md", ".docx", ".epub"]

# Crear directorios si no existen
DOCS_DIR.mkdir(exist_ok=True)





