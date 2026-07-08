# Search the vector database and return the most relevant chunks.
from src.rag.d_vector_store import VectorStore

class RetrieverService:

    def __init__(self):
        self.vector_store = VectorStore().vector_store  #This gives us access to Chroma.

        self.retriever = self.vector_store.as_retriever(   # This is one of LangChain's nicest abstractions., 
            search_kwargs={ #Top 4 most relevant chunks
                "k": 4 
            }
        )

    def retrieve(self, question: str):
        return self.retriever.invoke(question)
    


'''
as_retriever()

This is one of LangChain's nicest abstractions.

Instead of

    Chroma
    ↓
    Similarity Search
    ↓
    Sorting
    ↓
    Top Results

LangChain wraps everything inside
    retriever

Now we simply write
    retriever.invoke(question)

'''