from google import genai
from config import GEMINI_API_KEY

class GeminiClient:
    def __init__(self): #Constructor
        self.client= genai.Client(api_key=GEMINI_API_KEY) #This creates a connection object., The client lets us communicate with Google's servers.

    def chat(self,message:str)-> str:
        resp=self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message,
        )
        return resp.text