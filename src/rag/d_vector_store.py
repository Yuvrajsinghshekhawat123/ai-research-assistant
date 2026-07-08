from langchain_chroma import Chroma
from src.rag.c_embedding_service import EmbeddingService

from src.rag.a_document_loader import DocumentLoader
from src.rag.b_text_splitter import TextSplitter

class VectorStore:

    def __init__(self):
        embedding_model = EmbeddingService().get_embeddings()

        self.vector_store = Chroma(
            collection_name="knowledge_base",
            embedding_function=embedding_model,
            persist_directory="./data/chroma_db",
        )

    def add_documents(self, documents):
        self.vector_store.add_documents(documents)


# loader = DocumentLoader()
# docs = loader.load("data/java_introduction.pdf")

# splitter = TextSplitter()
# chunks = splitter.split(docs)

# store = VectorStore()

# store.add_documents(chunks)

# print("Documents stored!")