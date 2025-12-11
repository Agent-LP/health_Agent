"""
Ejemplo de uso programático del sistema RAG de consejos de salud
"""
from document_loader import load_all_documents, split_documents
from rag_system import HealthRAGSystem
import config


def example_basic_usage():
    """
    Ejemplo básico de uso del sistema
    """
    print("Ejemplo 1: Uso básico\n")
    
    # Cargar y procesar documentos
    documents = load_all_documents()
    doc_splits = split_documents(documents)
    
    # Inicializar sistema RAG
    rag_system = HealthRAGSystem(doc_splits)
    
    # Hacer una pregunta
    question = "¿Cuáles son los mejores hábitos para dormir bien?"
    answer = rag_system.ask(question)
    
    print(f"Pregunta: {question}")
    print(f"Respuesta: {answer}\n")


def example_custom_k():
    """
    Ejemplo usando un número diferente de documentos
    """
    print("Ejemplo 2: Usando más documentos\n")
    
    documents = load_all_documents()
    doc_splits = split_documents(documents)
    rag_system = HealthRAGSystem(doc_splits)
    
    # Consultar con más documentos (8 en lugar del default de 4)
    question = "¿Qué ejercicios son mejores para la salud cardiovascular?"
    answer = rag_system.ask(question, k=8)
    
    print(f"Pregunta: {question}")
    print(f"Respuesta: {answer}\n")


def example_get_documents():
    """
    Ejemplo de cómo obtener los documentos relevantes
    """
    print("Ejemplo 3: Ver documentos relevantes\n")
    
    documents = load_all_documents()
    doc_splits = split_documents(documents)
    rag_system = HealthRAGSystem(doc_splits)
    
    question = "¿Cómo mejorar la nutrición?"
    
    # Obtener documentos relevantes
    relevant_docs = rag_system.get_relevant_documents(question, k=5)
    
    print(f"Pregunta: {question}")
    print(f"\nDocumentos relevantes encontrados ({len(relevant_docs)}):")
    for i, doc in enumerate(relevant_docs, 1):
        source = doc.metadata.get("source", "Desconocido")
        preview = doc.page_content[:100] + "..." if len(doc.page_content) > 100 else doc.page_content
        print(f"\n{i}. {source}")
        print(f"   Preview: {preview}")


if __name__ == "__main__":
    try:
        example_basic_usage()
        example_custom_k()
        example_get_documents()
    except Exception as e:
        print(f"Error: {e}")
        print("\nAsegúrate de tener documentos en la carpeta 'docs'")





