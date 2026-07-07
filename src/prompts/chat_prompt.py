from models.chat_message import ChatMessage


class ChatPromptBuilder:

    def build(self, messages: list[ChatMessage]) -> str:
        prompt = ""

        for message in messages:
            role = message.role.value.capitalize()
            prompt += f"{role}: {message.content}\n"

        prompt += "Assistant:"

        return prompt
    


'''
What Should It Do?

Input

[
    ChatMessage(role="user", content="Hello"),
    ChatMessage(role="assistant", content="Hi"),
    ChatMessage(role="user", content="What is Java?")
]

Output

User: Hello

Assistant: Hi

User: What is Java?

Assistant:

Notice the last line:-
    Assistant:

Why?
Because we're telling Gemini:
"Now it's your turn to continue the conversation."

'''

