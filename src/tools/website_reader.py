import re
import requests
from bs4 import BeautifulSoup
from readability import Document
from langchain_core.tools import tool


class WebsiteReaderTool:
    """
    Opens a webpage and extracts the main readable content.
    Removes scripts, styles, navigation, headers, footers, and ads where possible.
    """

    def __init__(self, timeout: int = 10, max_chars: int = 8000):
        self.timeout = timeout
        self.max_chars = max_chars

    def read(self, url: str) -> str:
        if not url.strip():
            return "No URL provided."

        try:
            response = requests.get(
                url,
                timeout=self.timeout,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 Chrome/120 Safari/537.36"
                    )
                },
            )
            response.raise_for_status()
        except requests.RequestException as error:
            return f"Failed to read website: {error}"

        try:
            document = Document(response.text)
            title = document.title()
            html = document.summary()
        except Exception:
            title = "Untitled page"
            html = response.text

        soup = BeautifulSoup(html, "html.parser")

        for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "aside"]):
            tag.decompose()

        text = soup.get_text(separator="\n")
        text = self._clean_text(text)

        if not text:
            return "No readable content found on this webpage."

        if len(text) > self.max_chars:
            text = text[: self.max_chars] + "\n\n[Content truncated because the page is very long.]"

        return f"Title: {title}\nURL: {url}\n\nContent:\n{text}"

    def _clean_text(self, text: str) -> str:
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r"[ \t]+", " ", text)
        return text.strip()


website_reader_service = WebsiteReaderTool()


@tool
def website_reader(url: str) -> str:
    """
    Open a webpage URL and extract clean readable content.
    Use this after web_search finds a useful URL.
    """
    return website_reader_service.read(url)