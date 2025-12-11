"""
Módulo para cargar y procesar documentos de salud desde la carpeta docs
"""
from pathlib import Path
from typing import List
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
    UnstructuredWordDocumentLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import config


def load_document(file_path: Path) -> List[Document]:
    """
    Carga un documento según su extensión
    
    Args:
        file_path: Ruta al archivo
        
    Returns:
        Lista de documentos cargados
    """
    suffix = file_path.suffix.lower()
    
    try:
        if suffix == ".pdf":
            loader = PyPDFLoader(str(file_path))
        elif suffix == ".txt":
            loader = TextLoader(str(file_path), encoding="utf-8")
        elif suffix == ".md":
            loader = UnstructuredMarkdownLoader(str(file_path))
        elif suffix == ".docx":
            loader = UnstructuredWordDocumentLoader(str(file_path))
        else:
            raise ValueError(f"Tipo de archivo no soportado: {suffix}")
        
        documents = loader.load()
        # Agregar metadata con el nombre del archivo
        for doc in documents:
            doc.metadata["source"] = file_path.name
            doc.metadata["file_path"] = str(file_path)
        
        return documents
    except Exception as e:
        print(f"Error al cargar {file_path}: {e}")
        return []


def load_all_documents(docs_dir: Path = None) -> List[Document]:
    """
    Carga todos los documentos de la carpeta docs
    
    Args:
        docs_dir: Directorio con los documentos (por defecto usa config.DOCS_DIR)
        
    Returns:
        Lista de todos los documentos cargados
    """
    if docs_dir is None:
        docs_dir = config.DOCS_DIR
    
    all_documents = []
    
    # Buscar todos los archivos soportados
    for file_type in config.SUPPORTED_FILE_TYPES:
        for file_path in docs_dir.glob(f"*{file_type}"):
            print(f"Cargando: {file_path.name}")
            documents = load_document(file_path)
            all_documents.extend(documents)
    
    print(f"Total de documentos cargados: {len(all_documents)}")
    return all_documents


def split_documents(documents: List[Document]) -> List[Document]:
    """
    Divide los documentos en chunks más pequeños
    
    Args:
        documents: Lista de documentos a dividir
        
    Returns:
        Lista de chunks de documentos
    """
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
    )
    
    doc_splits = text_splitter.split_documents(documents)
    print(f"Documentos divididos en {len(doc_splits)} chunks")
    return doc_splits





