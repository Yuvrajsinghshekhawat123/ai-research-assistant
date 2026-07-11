from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END

from src.llm import GeminiClient
from src.models.research_result import ResearchResult
from src.tools.pdf_search import pdf_search
from src.tools.web_search import web_search
from src.tools.website_reader import website_reader


class ResearchState(TypedDict):
    question: str
    history: list
    pdf_context: str
    web_results: str
    website_content: str
    tools_used: List[str]
    web_urls: List[str]
    evidence: List[str]
    answer: str
    answer_source: str


class ResearchGraph:
    def __init__(self):
        self.llm = GeminiClient()
        self.graph = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(ResearchState)

        workflow.add_node("chat", self._chat_node)
        workflow.add_node("pdf_search", self._pdf_search_node)
        workflow.add_node("web_search", self._web_search_node)
        workflow.add_node("website_reader", self._website_reader_node)
        workflow.add_node("answer", self._answer_node)

        workflow.add_conditional_edges(
            START,
            self._route_from_start,
            {
                "chat": "chat",
                "pdf_search": "pdf_search",
            },
        )

        workflow.add_edge("chat", END)

        workflow.add_conditional_edges(
            "pdf_search",
            self._route_after_pdf,
            {
                "answer": "answer",
                "web_search": "web_search",
            },
        )

        workflow.add_edge("web_search", "website_reader")
        workflow.add_edge("website_reader", "answer")
        workflow.add_edge("answer", END)

        return workflow.compile()

    def run(self, question: str, history=None) -> ResearchResult:
        if history is None:
            history = []

        initial_state = {
            "question": question,
            "history": history,
            "pdf_context": "",
            "web_results": "",
            "website_content": "",
            "tools_used": [],
            "web_urls": [],
            "evidence": [],
            "answer": "",
            "answer_source": "",
        }

        final_state = self.graph.invoke(initial_state)

        return ResearchResult(
            answer=final_state["answer"],
            tools_used=final_state["tools_used"],
            pdf_context_used=final_state["answer_source"] == "pdf",
            web_urls=final_state["web_urls"],
            evidence=final_state["evidence"],
        )

    def _route_from_start(self, state: ResearchState) -> str:
        question = state["question"].lower().strip()

        greetings = {"hi", "hello", "hey", "hii", "hy"}

        if question in greetings:
            return "chat"

        return "pdf_search"

    def _chat_node(self, state: ResearchState):
        answer = self.llm.chat(state["question"])

        return {
            "answer": answer,
            "answer_source": "chat",
        }

    def _pdf_search_node(self, state: ResearchState):
        context = pdf_search.invoke({"question": state["question"]})

        if context is None:
            context = ""

        return {
            "pdf_context": context,
            "tools_used": state["tools_used"] + ["pdf_search"],
            "evidence": state["evidence"] + ([context] if context.strip() else []),
        }

    def _route_after_pdf(self, state: ResearchState) -> str:
        if self._is_pdf_context_enough(
            question=state["question"],
            context=state["pdf_context"],
        ):
            return "answer"

        return "web_search"

    def _web_search_node(self, state: ResearchState):
        query = self._build_search_query(state["question"])
        results = web_search.invoke({"query": query})

        if results is None:
            results = ""

        url = self._extract_best_url(results)

        return {
            "web_results": results,
            "web_urls": state["web_urls"] + ([url] if url else []),
            "tools_used": state["tools_used"] + ["web_search"],
            "evidence": state["evidence"] + ([results] if results.strip() else []),
        }

    def _website_reader_node(self, state: ResearchState):
        if not state["web_urls"]:
            return {
                "website_content": "",
                "tools_used": state["tools_used"],
            }

        url = state["web_urls"][0]
        content = website_reader.invoke({"url": url})

        if content is None:
            content = ""

        return {
            "website_content": content,
            "tools_used": state["tools_used"] + ["website_reader"],
            "evidence": state["evidence"] + ([content] if content.strip() else []),
        }

    def _answer_node(self, state: ResearchState):
        evidence = state["pdf_context"]
        answer_source = "pdf"

        if state["website_content"]:
            evidence = state["website_content"]
            answer_source = "web"
        elif state["web_results"]:
            evidence = state["web_results"]
            answer_source = "web"

        prompt = f"""
You are an AI Research Assistant.

Answer the user question using only the evidence below.
If the evidence is not enough, say you could not find enough reliable information.
Do not invent facts.
If web URLs are available, include them as sources.

Question:
{state["question"]}

Evidence:
{evidence}

Sources:
{state["web_urls"]}

Final Answer:
"""

        answer = self.llm.chat(prompt)

        return {
            "answer": answer,
            "answer_source": answer_source,
        }

    def _is_pdf_context_enough(self, question: str, context: str) -> bool:
        if not context or not context.strip():
            return False

        prompt = f"""
Question:
{question}

PDF Context:
{context}

Can the question be answered completely and directly using ONLY this PDF context?

Important:
- If the context is about another topic, reply NO.
- If the question asks about a topic not present in the context, reply NO.
- If the question asks for comparison and one item is missing, reply NO.
- Reply with only YES or NO.

Answer:
"""

        response = self.llm.chat(prompt).strip().upper()
        return response.startswith("YES")

    def _build_search_query(self, question: str) -> str:
        clean_question = question.strip()

        replacements = {
            "cpp": "C++ programming language",
            "c++": "C++ programming language",
            "langchian": "LangChain",
            "crewai": "CrewAI",
        }

        lower_question = clean_question.lower()

        for wrong, correct in replacements.items():
            if wrong in lower_question:
                lower_question = lower_question.replace(wrong, correct)

        return lower_question

    def _extract_best_url(self, search_results: str):
        blocked_domains = [
            "whatsapp.com",
            "facebook.com",
            "instagram.com",
            "twitter.com",
            "x.com",
            "youtube.com",
            "pinterest.com",
        ]

        for line in search_results.splitlines():
            if line.startswith("URL:"):
                url = line.replace("URL:", "").strip()

                if not url:
                    continue

                if any(domain in url for domain in blocked_domains):
                    continue

                return url

        return None