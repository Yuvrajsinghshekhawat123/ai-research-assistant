from models.chat_message import ChatMessage


class ConversationMemory:
    def __init__(self):
        self.messages: list[ChatMessage] = []

    def add_message(self, message: ChatMessage):
        self.messages.append(message)

    def get_messages(self) -> list[ChatMessage]:
        return self.messages

    def clear(self):
        self.messages.clear()



'''
Part 4: = []

This creates an empty list.

[]

means

No messages yet.

Later

[]

becomes

[
   [
    ChatMessage(
        role="user",
        content="Hello",
        timestamp="10:30"
    ),

    ChatMessage(
        role="assistant",
        content="Hi!",
        timestamp="10:31"
    ),

    ChatMessage(
        role="user",
        content="What is Java?",
        timestamp="10:32"
    )
]
]
'''