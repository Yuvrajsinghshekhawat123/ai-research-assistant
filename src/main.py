from src.config import GEMINI_API_KEY
from src.services.chat_service import ChatService


def main():

    print("=" * 40)
    print("🤖 AI Research Assistant")
    print("=" * 40)
    chat_service = ChatService()
    
    while True:
        user_input = input("\nYou: ")
        response=chat_service.chat(user_input)
        result = chat_service.last_research_result



        if user_input.lower() == "exit":
            print("\nGoodbye 👋")
            break



        print(f"\nAI:\n{response}")

        
        if result:
            print("\n--- Research Trace ---")
            print("Tools used:", result.tools_used)
            print("PDF context used:", result.pdf_context_used)
            print("Web URLs:", result.web_urls)
            print("Evidence count:", len(result.evidence))



if __name__ == "__main__":
    main()

