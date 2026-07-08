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



        if user_input.lower() == "exit":
            print("\nGoodbye 👋")
            break



        print(f"\nAI:\n{response}")


if __name__ == "__main__":
    main()

