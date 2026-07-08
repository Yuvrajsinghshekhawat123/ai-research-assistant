from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.rag.a_document_loader import DocumentLoader


class TextSplitter:

    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )

    def split(self, documents):
        return self.splitter.split_documents(documents)
    


# loader=DocumentLoader()
# docs=loader.load("../../data/java_introduction.pdf")
# splitter=TextSplitter();
# chunks = splitter.split(docs)

# print(len(chunks))
# print(chunks[0].page_content)