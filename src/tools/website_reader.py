import re
from bs4 import BeautifulSoup
from readability import Document
from langchain_core.tools import tool
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


class WebsiteReaderTool:
    """
    Opens a webpage using Playwright, extracts readable content,
    removes unwanted page elements, and returns clean text.
    """

    def __init__(self, timeout: int = 15, max_chars: int = 8000):
        self.timeout = timeout
        self.max_chars = max_chars

    def read(self, url: str) -> str:
        if not url.strip():
            return "No URL provided."

        try:
            html = self._load_page_with_playwright(url)
        except Exception as error:
            return f"Failed to read website: {error}"

        try:
            document = Document(html)
            title = document.title()
            main_html = document.summary()
        except Exception:
            title = "Untitled page"
            main_html = html

        soup = BeautifulSoup(main_html, "html.parser")
        self._remove_unwanted_elements(soup)

        text = soup.get_text(separator="\n")
        text = self._clean_text(text)

        if not text:
            return "No readable content found on this webpage."

        if len(text) > self.max_chars:
            text = text[: self.max_chars] + "\n\n[Content truncated because the page is very long.]"

        return f"Title: {title}\nURL: {url}\n\nContent:\n{text}"

    def _load_page_with_playwright(self, url: str) -> str:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)

            page = browser.new_page(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 Chrome/120 Safari/537.36"
                )
            )

            try:
                page.goto(
                    url,
                    wait_until="domcontentloaded",
                    timeout=self.timeout * 1000,
                )

                page.wait_for_timeout(2000)

                html = page.content()
                return html

            except PlaywrightTimeoutError:
                return page.content()

            finally:
                browser.close()

    def _remove_unwanted_elements(self, soup: BeautifulSoup) -> None:
        unwanted_tags = [
            "script",
            "style",
            "noscript",
            "header",
            "footer",
            "nav",
            "aside",
            "form",
            "button",
            "iframe",
            "svg",
        ]

        for tag in soup(unwanted_tags):
            tag.decompose()

        unwanted_keywords = [
            "cookie",
            "banner",
            "popup",
            "modal",
            "advert",
            "ads",
            "sidebar",
            "newsletter",
            "subscribe",
            "social",
            "comment",
            "footer",
            "header",
            "nav",
            "menu",
        ]

        for element in soup.find_all(True):
            element_id = " ".join(element.get("id", "").lower().split())
            element_class = " ".join(element.get("class", [])).lower()

            combined = f"{element_id} {element_class}"

            if any(keyword in combined for keyword in unwanted_keywords):
                element.decompose()

    def _clean_text(self, text: str) -> str:
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r" +\n", "\n", text)
        return text.strip()


website_reader_service = WebsiteReaderTool()


@tool
def website_reader(url: str) -> str:
    """
    Open a webpage URL using Playwright and extract clean readable content.
    Use this after web_search finds a useful URL.
    """
    return website_reader_service.read(url)