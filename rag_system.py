"""
Sistema RAG completo para consejos de salud
"""
from typing import List, Optional
from langchain_community.vectorstores import SKLearnVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough

import config
from helpers import create_and_persist, load_embeddings
from prompts import HEALTH_ADVICE_PROMPT


class HealthRAGSystem:
    """
    Sistema RAG para proporcionar consejos de salud basados en documentos
    """
    
    def __init__(
        self,
        documents: List[Document],
        k: int = None,
        score_threshold: Optional[float] = None
    ):
        """
        Inicializa el sistema RAG
        
        Args:
            documents: Lista de documentos a indexar
            k: Número de documentos a recuperar (por defecto usa config.RETRIEVER_K)
            score_threshold: Umbral mínimo de relevancia (opcional)
        """
        self.k = k or config.RETRIEVER_K
        self.score_threshold = score_threshold or config.RETRIEVER_SCORE_THRESHOLD
        
        # Inicializar embeddings
        print("Inicializando modelo de embeddings...")
        self.embedding = HuggingFaceEmbeddings(
            model_name=config.EMBEDDING_MODEL
        )
        
        # Crear vectorstore
        print("Creando índice vectorial...")
        # Si ya existe el vectorstore, cargarlo
        vectorstore_exists = config.VECTORSTORE_DIR.is_dir()
        vectorstore_empty = (
            not vectorstore_exists or
            (vectorstore_exists and not any(config.VECTORSTORE_DIR.iterdir()))
        )
        persist_path = config.VECTORSTORE_DIR / "vectorstore.json"
        if vectorstore_exists and not vectorstore_empty:
            print("🔄 Cargando vectorstore local...")
            vectorstore = load_embeddings(self.embedding, persist_path, "json")
            # Configurar retriever
            self.retriever = vectorstore.as_retriever(
                search_kwargs={"k": self.k}
            )
        else:
            print("📌 Generando vectorstore...")
            config.VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
            
            vectorstore = create_and_persist(documents, persist_path, "json", self.embedding)
            # Configurar retriever
            self.retriever = vectorstore.as_retriever(
                search_kwargs={"k": self.k}
            )
        
        # Inicializar LLM
        print(f"Inicializando modelo LLM: {config.LLM_MODEL}")
        self.llm = ChatOllama(
            model=config.LLM_MODEL,
            temperature=config.LLM_TEMPERATURE,
        )
        
        # Crear cadena RAG con formateo de documentos
        def format_docs(docs):
            return "\n\n---\n\n".join([f"[Fuente: {doc.metadata.get('source', 'Desconocido')}]\n{doc.page_content}" for doc in docs])
        
        self.rag_chain = (
            {
                "question": RunnablePassthrough(),
                "documents": lambda x: format_docs(self.retriever.invoke(x["question"]))
            }
            | HEALTH_ADVICE_PROMPT
            | self.llm
            | StrOutputParser()
        )
        
        print("Sistema RAG inicializado correctamente")
    
    def _format_documents(self, docs: List[Document]) -> str:
        """
        Formatea los documentos recuperados para el prompt
        
        Args:
            docs: Lista de documentos
            
        Returns:
            String formateado con los documentos
        """
        formatted = []
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get("source", "Desconocido")
            formatted.append(f"[Documento {i} - Fuente: {source}]\n{doc.page_content}")
        return "\n\n---\n\n".join(formatted)
    
    def ask(self, question: str, k: Optional[int] = None) -> str:
        """
        Hace una pregunta al sistema RAG
        
        Args:
            question: Pregunta del usuario
            k: Número de documentos a recuperar (opcional, usa el valor por defecto si no se especifica)
            
        Returns:
            Respuesta del sistema
        """
        # Función para formatear documentos
        def format_docs(docs):
            return "\n\n---\n\n".join([f"[Fuente: {doc.metadata.get('source', 'Desconocido')}]\n{doc.page_content}" for doc in docs])
        
        # Si se especifica un k diferente, usar ese retriever temporalmente
        if k is not None and k != self.k:
            temp_retriever = self.vectorstore.as_retriever(
                search_kwargs={"k": k}
            )
            # Crear cadena temporal con el nuevo retriever
            temp_rag_chain = (
                {
                    "question": RunnablePassthrough(),
                    "documents": lambda x: format_docs(temp_retriever.invoke(x["question"]))
                }
                | HEALTH_ADVICE_PROMPT
                | self.llm
                | StrOutputParser()
            )
            answer = temp_rag_chain.invoke({"question": question})
        else:
            # Usar la cadena normal
            answer = self.rag_chain.invoke({"question": question})
        
        return answer
    
    def get_relevant_documents(self, question: str, k: Optional[int] = None) -> List[Document]:
        """
        Obtiene los documentos más relevantes para una pregunta
        
        Args:
            question: Pregunta del usuario
            k: Número de documentos a recuperar
            
        Returns:
            Lista de documentos relevantes
        """
        if k is None:
            k = self.k
        
        docs = self.retriever.invoke(question)
        return docs[:k] if len(docs) > k else docs

