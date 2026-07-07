from models.chat_message import ChatMessage


class ConversationMemory:
    def __init__(self):
        self.messages: list[ChatMessage] = []

    def add_message(self, message: ChatMessage):
        self.messages.append(message)

    def get_messages(self) -> list[ChatMessage]:
        return self.messages.copy();

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



"""
Q- why we do .copy():

What if we return the original list?
def get_messages(self):
    return self.messages

Now someone does:
msgs = chat_service.get_messages()

What is msgs?
It is not a new list.
It is another variable pointing to the same list.


Now imagine someone writes
msgs.clear()
What happens?

msgs
 │
 ▼
[]

Since both point to the same list,

self.messages
also becomes

[]

😱 The chatbot's memory is deleted!
"""