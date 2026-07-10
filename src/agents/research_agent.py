from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

from src.llm import GeminiClient
from src.models.research_result import ResearchResult
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

    def run(self, question: str, history=None) -> ResearchResult:
        if history is None:
            history = []

        messages = list(history)
        messages.append(HumanMessage(content=question))

        response = self.agent.invoke(
            {
                "messages": messages
            }
        )

        final_content = response["messages"][-1].content
        answer = self._extract_text(final_content)

        tools_used = self._extract_tools_used(response)
        urls_visited = self._extract_urls(response)
        evidence = self._extract_evidence(response)

        return ResearchResult(
            answer=answer,
            tools_used=tools_used,
            pdf_context_used="pdf_search" in tools_used,
            web_urls=urls_visited,
            evidence=evidence,
        )

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

    def _extract_tools_used(self, response) -> list[str]:
        tools = []

        for message in response["messages"]:
            tool_name = getattr(message, "name", None)

            if tool_name:
                tools.append(tool_name)

        return tools

    def _extract_urls(self, response) -> list[str]:
        urls = []

        for message in response["messages"]:
            content = getattr(message, "content", "")

            if isinstance(content, str):
                for line in content.splitlines():
                    if line.startswith("URL:"):
                        urls.append(line.replace("URL:", "").strip())

        return urls

    def _extract_evidence(self, response) -> list[str]:
        evidence = []

        for message in response["messages"]:
            tool_name = getattr(message, "name", None)

            if tool_name in ["pdf_search", "web_search", "website_reader"]:
                content = getattr(message, "content", "")

                if isinstance(content, str) and content.strip():
                    evidence.append(content[:1000])

        return evidence