# Convert your custom messages into LangChain messages before passing them to the prompt.
from langchain_core.messages import HumanMessage, AIMessage
from src.models.role import Role


class CustomObjToLangchainMessage:

    @staticmethod
    def convert_history(history):
        messages = []

        for message in history:

            if message.role == Role.USER:
                messages.append(
                    HumanMessage(content=message.content)
                )

            elif message.role == Role.ASSISTANT:
                messages.append(
                    AIMessage(content=message.content)
                )

        return messages