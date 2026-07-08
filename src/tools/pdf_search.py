from langchain_core.tools import tool
from src.rag.f_rag_service import RAGService


rag_service = RAGService()


@tool
def pdf_search(question: str) -> str:
    """
    Search the local PDF knowledge base using ChromaDB/RAG.
    Use this first before searching the web.
    """
    context = rag_service.get_context(question)

    if not context:
        return ""

    return context