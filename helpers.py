from langchain_community.vectorstores.sklearn import SKLearnVectorStore


def create_and_persist(doc_splits, persist_path, serializer, embedding):
        # crea el vectorstore desde documentos y embeddings
        vectorstore = SKLearnVectorStore.from_documents(
            documents=doc_splits,
            embedding=embedding,
            persist_path=persist_path,
            serializer=serializer,
        )
        # persistir usando la API actual
        print("💾 Persistiendo vectorstore en:", persist_path)
        vectorstore.persist()
        return vectorstore


def load_embeddings(embedding, persist_path, serializer):
    print("🔄 Cargando vectorstore desde persist_path...")
    vectorstore = SKLearnVectorStore(
        embedding=embedding,
        persist_path=persist_path,
        serializer=serializer,
    )
    
    prueba = vectorstore.similarity_search("test", k=1)
    print(prueba)
    return vectorstore
    # opcional: probar una búsqueda rápida para asegurarnos que está OK