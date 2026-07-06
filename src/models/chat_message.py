'''
The word 'Model' here does not mean an AI model like Gemini or GPT.
It means a data model—a class whose job is to represent and organize data.



Without a Data Model

Suppose a user sends:

Hello

You could store it like this:
    # message = "Hello"
But after some time, you also need to know:
    Who sent it?
    When was it sent?
    Which conversation does it belong to?
A simple string can't store all of that.





So we create a Model
We create a class that groups all related information together.

        from dataclasses import dataclass
        from datetime import datetime

        @dataclass
        class ChatMessage:
            role: str
            content: str
            timestamp: datetime

Now instead of just:
message = "Hello"

you create an object:

msg = ChatMessage(
    role="user",
    content="Hello",
    timestamp=datetime.now()
)



messages = [
    ChatMessage(
        role="user",
        content="Hello",
        timestamp="9:30"
    ),

    ChatMessage(
        role="assistant",
        content="Hi! How can I help?",
        timestamp="9:31"
    ),

    ChatMessage(
        role="user",
        content="What is Java?",
        timestamp="9:32"
    )
]




Why use Models?

Imagine you build an AI chatbot.

Later you want to save chats in a database.

A table might look like this:

conversation_id	        role	        content	        timestamp
1	                    user	        Hello	        9:30
1	                    assistant	    Hi!	            9:31
1	                    user	        What is Java?	9:32

Each row can be represented by one ChatMessage object.

'''



'''
What is @dataclass?

This is one of Python's best features.
Without it,

we'd have to write
        class ChatMessage:

            def __init__(self, role, content):
                self.role = role
                self.content = content

                
Lots of boilerplate.
'''

from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class ChatMessage:
    role: str
    content: str
    timestamp: datetime =field(default_factory=datetime.now)


"""
Why do we use field(default_factory=...) instead of datetime.now()?

Many beginners try this:

timestamp: datetime = datetime.now()   # ❌ Not recommended

This calls datetime.now() once, when the class is defined. Every object would get the same timestamp.

Instead:

timestamp: datetime = field(default_factory=datetime.now)

means:

"Whenever a new ChatMessage object is created, call datetime.now() and use that value."
"""

