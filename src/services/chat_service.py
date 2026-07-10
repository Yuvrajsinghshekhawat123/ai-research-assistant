'''
This is one of the most important folders.

Question:

Who should talk to Gemini?

main.py?

No.

Instead

main.py

↓

ChatService

↓

GeminiClient

↓

Gemini

Why?

Because tomorrow

ChatService will do

    Memory
    Validation
    Prompt building
    Logging

before calling Gemini.

'''


from src.memory import ConversationMemory
from src.prompts.chat_prompt import ChatPromptBuilder
 
from src.models.chat_message import ChatMessage
from src.models.role import Role
from src.utils.LangChain_messages import CustomObjToLangchainMessage
from src.agents.research_agent import ResearchAgent


class ChatService:

    def __init__(self):
        self.memory = ConversationMemory()
        self.prompt_builder = ChatPromptBuilder()
        self.research_agent = ResearchAgent()
        self.last_research_result = None
         

    def chat(self, user_input: str) -> str:
        history = CustomObjToLangchainMessage.convert_history(
            self.memory.get_messages()
        )

        # catch quota errors so your app does not crash:
        try:
            research_result = self.research_agent.run(
                question=user_input,
                history=history
            )
        except Exception as error:
            error_text = str(error)

            if "RESOURCE_EXHAUSTED" in error_text or "429" in error_text:
                return "Gemini API quota is exhausted. Please wait and try again later, or switch to another Gemini model/API key."

            return f"AI service error: {error}"
        


        response = research_result.answer
        self.last_research_result = research_result

        user_message = ChatMessage(
            role=Role.USER,
            content=user_input
        )

        assistant_message = ChatMessage(
            role=Role.ASSISTANT,
            content=response

        )

        self.memory.add_message(user_message)
        self.memory.add_message(assistant_message)

        return response




"""
Why Create These Objects Here?

Question:

Should main.py create

ConversationMemory()

GeminiClient()

ChatPromptBuilder()

No.

Because they're part of the chat system.

So ChatService owns them.

Think of it like a car.

Car

↓

Engine

↓

Gearbox

↓

Battery

When you buy a car,

you don't buy the engine separately.

The car contains everything.

"""