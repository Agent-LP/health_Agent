"""
Aplicación principal del sistema RAG para consejos de salud
"""
from document_loader import load_all_documents, split_documents
from rag_system import HealthRAGSystem
import config


def initialize_rag_system():
    """
    Inicializa el sistema RAG cargando documentos y creando el índice
    
    Returns:
        HealthRAGSystem inicializado
    """
    print("=" * 60)
    print("Sistema RAG de Consejos de Salud")
    print("=" * 60)
    
    # Cargar documentos
    print("\n1. Cargando documentos...")
    documents = load_all_documents()
    
    if not documents:
        raise ValueError(
            f"No se encontraron documentos en {config.DOCS_DIR}. "
            f"Por favor, agrega archivos PDF, TXT, MD o DOCX en esa carpeta."
        )
    
    # Dividir documentos en chunks
    print("\n2. Procesando documentos...")
    doc_splits = split_documents(documents)
    
    # Inicializar sistema RAG
    print("\n3. Inicializando sistema RAG...")
    rag_system = HealthRAGSystem(doc_splits)
    
    print("\n" + "=" * 60)
    print("Sistema listo para usar!")
    print("=" * 60 + "\n")
    
    return rag_system


def interactive_mode(rag_system: HealthRAGSystem):
    """
    Modo interactivo para hacer preguntas al sistema
    
    Args:
        rag_system: Sistema RAG inicializado
    """
    print("\nModo interactivo activado.")
    print("Escribe 'salir' o 'exit' para terminar.")
    print("Escribe 'docs N' antes de tu pregunta para cambiar el número de documentos a consultar (ej: 'docs 6')\n")
    
    current_k = config.RETRIEVER_K
    
    while True:
        try:
            question = input("\nTu pregunta: ").strip()
            
            if question.lower() in ['salir', 'exit', 'quit']:
                print("\n¡Hasta luego!")
                break
            
            if not question:
                continue
            
            # Verificar si el usuario quiere cambiar el número de documentos
            if question.lower().startswith('docs '):
                try:
                    new_k = int(question.split()[1])
                    current_k = new_k
                    print(f"✓ Número de documentos cambiado a {current_k}")
                    continue
                except (IndexError, ValueError):
                    print("Formato incorrecto. Usa: 'docs N' (ej: 'docs 6')")
                    continue
            
            # Obtener respuesta
            print("\nBuscando información relevante...")
            answer = rag_system.ask(question, k=current_k)
            
            print(f"\n{'='*60}")
            print("RESPUESTA:")
            print(f"{'='*60}")
            print(answer)
            print(f"{'='*60}")
            
            # Mostrar documentos consultados (opcional)
            relevant_docs = rag_system.get_relevant_documents(question, k=current_k)
            print(f"\n📚 Documentos consultados ({len(relevant_docs)}):")
            for i, doc in enumerate(relevant_docs, 1):
                source = doc.metadata.get("source", "Desconocido")
                print(f"  {i}. {source}")
            
        except KeyboardInterrupt:
            print("\n\n¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


def main():
    """
    Función principal
    """
    try:
        # Inicializar sistema
        rag_system = initialize_rag_system()
        
        # Modo interactivo
        interactive_mode(rag_system)
        
    except Exception as e:
        print(f"\n❌ Error al inicializar el sistema: {e}")
        print("\nAsegúrate de que:")
        print("1. Hay documentos en la carpeta 'docs'")
        print("2. Ollama está corriendo y tiene el modelo instalado")
        print("3. Tienes conexión a internet para descargar el modelo de embeddings")


if __name__ == "__main__":
    main()





