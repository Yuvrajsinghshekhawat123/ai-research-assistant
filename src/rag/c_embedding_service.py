from langchain_google_genai import GoogleGenerativeAIEmbeddings
from src.config import GEMINI_API_KEY
from src.rag.a_document_loader import DocumentLoader
from src.rag.b_text_splitter import TextSplitter


class EmbeddingService:

    def __init__(self):
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="gemini-embedding-2-preview"
        )

    def get_embeddings(self):
        return self.embeddings
    

# loader=DocumentLoader()
# docs=loader.load("data/java_introduction.pdf")
# splitter=TextSplitter()
# chunks = splitter.split(docs)

# embedding_service = EmbeddingService()
# embeddings = embedding_service.get_embeddings()
# vector = embeddings.embed_query("What is Java?")

# print(len(vector))