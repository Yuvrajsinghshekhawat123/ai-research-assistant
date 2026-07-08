from typing import List, Dict
from ddgs import DDGS
from langchain_core.tools import tool


class WebSearchTool:
    """
    Searches the web using DDGS.
    Returns titles, URLs, and snippets for the best results.
    """

    def __init__(self, max_results: int = 5):
        self.max_results = max_results

    def search(self, query: str) -> str:
        if not query.strip():
            return "No search query provided."

        results: List[Dict] = DDGS().text(
            query=query,
            region="us-en",
            safesearch="moderate",
            max_results=self.max_results,
            backend="auto",
        )

        if not results:
            return "No web search results found."

        formatted_results = []

        for index, result in enumerate(results, start=1):
            title = result.get("title", "No title")
            url = result.get("href") or result.get("url", "No URL")
            snippet = result.get("body", "No description available")

            formatted_results.append(
                f"{index}. {title}\nURL: {url}\nSummary: {snippet}"
            )

        return "\n\n".join(formatted_results)


web_search_service = WebSearchTool()

@tool   #@tool is a Python decorator used to convert a normal function into a tool that an AI agent (such as a LangChain agent) can call. ,, @tool tells LangChain that add() is a tool. ,,, The function's name, type hints, and docstring become part of the tool's metadata.,,, An LLM can decide when to call this tool.
def web_search(query: str) -> str:
    """
    Search the internet when the local PDF knowledge base does not contain enough information.
    Returns search results with titles, URLs, and short summaries.
    """
    result=web_search_service.search(query)
    # print(result)
    # print(20 * '=')
    return  result