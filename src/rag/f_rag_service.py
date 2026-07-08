"""
Responsibility of RAGService

It should:
    ✅ Receive a question
    ✅ Retrieve relevant documents
    ✅ Convert documents into context
    ✅ Return the context
Nothing else.

It should NOT:
    Call Gemini
    Build prompts
    Print answers
"""





from src.rag.e_retriever import RetrieverService

class RAGService:

    def __init__(self):
        self.retriever = RetrieverService()
    
    def get_context(self, question: str) -> str:
        documents = self.retriever.retrieve(question)

        texts = []
        for document in documents:
            texts.append(document.page_content)
        
        context = "\n\n".join(texts)

        return context
    

"""
documents = [
    Document(page_content="Java is an object-oriented language."),
    Document(page_content="JVM executes Java bytecode."),
    Document(page_content="JDK contains JRE and development tools.")
]

"""