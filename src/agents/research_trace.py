class ResearchTrace:
    def __init__(self):
        self.tools_used=[]
        self.pdf_context_used = False
        self.web_urls = []
        self.evidence = []
    
    def add_tool(self,tool_name:str):
        self.tools_used.append(tool_name)
    
    def mark_pdf_used(self):
        self.pdf_context_used = True

    def add_url(self, url: str):
        self.web_urls.append(url)

    def add_evidence(self, text: str):
        if text:
            self.evidence.append(text[:1000])