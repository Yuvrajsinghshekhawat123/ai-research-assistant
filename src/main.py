from config import GEMINI_API_KEY
from llm import GeminiClient




def main():
    chatbot=GeminiClient()
    print("=" * 40)
    print("🤖 AI Research Assistant")
    print("=" * 40)

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() == "exit":
            print("\nGoodbye 👋")
            break

        response = chatbot.chat(user_input)

        print(f"\nAI:\n{response}")


if __name__ == "__main__":
    main()
