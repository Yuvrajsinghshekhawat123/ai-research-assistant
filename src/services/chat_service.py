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
         

    def chat(self, user_input: str) -> str:
        # Step 1
        user_message = ChatMessage(
            role=Role.USER,
            content=user_input
        )

        # Step 2
        self.memory.add_message(user_message)

        # Step 3
        history = CustomObjToLangchainMessage.convert_history(
            self.memory.get_messages()
        )

        
        
        # Step 4
        # prompt = self.prompt_builder.build(history)
        response = self.research_agent.run(
            question=user_input,
            history=history
        )

        # Step 6
        assistant_message = ChatMessage(
            role=Role.ASSISTANT,
            content=response
        )

        # Step 7
        self.memory.add_message(assistant_message)

        # Step 8
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