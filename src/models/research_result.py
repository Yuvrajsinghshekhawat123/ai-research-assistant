from dataclasses import dataclass, field
from typing import List

@dataclass
class ResearchResult:
    answer: str
    tools_used: List[str] = field(default_factory=list)
    pdf_context_used: bool = False
    web_urls: List[str] = field(default_factory=list)
    evidence: List[str] = field(default_factory=list)


"""
ResearchResult(
    answer="...",
    tools_used=["pdf_search", "web_search"],
    web_urls=["https://..."],
    evidence=["..."]
)

"""