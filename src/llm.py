from langchain_google_genai import ChatGoogleGenerativeAI
from src.config import GEMINI_API_KEY


class GeminiClient:
    def __init__(self):
        self.model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=GEMINI_API_KEY,
            temperature=0,
        )

    def chat(self, message: str) -> str:
        response = self.model.invoke(message)
        return response.content