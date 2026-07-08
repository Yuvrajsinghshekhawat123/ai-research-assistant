from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

from src.llm import GeminiClient
from src.prompts.rag_prompt import RESEARCH_AGENT_SYSTEM_PROMPT
from src.tools.pdf_search import pdf_search
from src.tools.web_search import web_search
from src.tools.website_reader import website_reader


class ResearchAgent:

    def __init__(self):
        self.llm = GeminiClient()

        self.tools = [
            pdf_search,
            web_search,
            website_reader,
        ]

        self.agent = create_agent(
            model=self.llm.model,
            tools=self.tools,
            system_prompt=RESEARCH_AGENT_SYSTEM_PROMPT,
        )

    def run(self, question: str, history=None) -> str:
        if history is None:
            history = []

        messages = list(history)

        # Add question only if ChatService did not already add it to history
        if not messages:
            messages.append(HumanMessage(content=question))

        response = self.agent.invoke(
            {
                "messages": messages
            }
        )

        final_content = response["messages"][-1].content

        return self._extract_text(final_content)

    def _extract_text(self, content) -> str:
        if isinstance(content, str):
            return content

        if isinstance(content, list):
            text_parts = []

            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text_parts.append(item.get("text", ""))

            return "\n".join(text_parts).strip()

        return str(content)