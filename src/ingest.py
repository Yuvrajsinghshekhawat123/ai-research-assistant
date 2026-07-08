#  ← Run once to build/update the knowledge base

from src.rag.a_document_loader import DocumentLoader
from src.rag.b_text_splitter import TextSplitter
from src.rag.d_vector_store import VectorStore

def ingest():
    loader = DocumentLoader()
    docs = loader.load("data/CV.pdf")

    splitter = TextSplitter()
    chunks = splitter.split(docs)

    store = VectorStore()



    store.add_documents(chunks)

    print("Knowledge base created successfully!")


if __name__ == "__main__":
    ingest()