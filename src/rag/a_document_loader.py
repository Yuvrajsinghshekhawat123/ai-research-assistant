# Read a document and return LangChain Document objects.
"""
uv add langchain-community
uv add pypdf


Why Document instead of str?
Problem with using str

Suppose you read a PDF.

Page 1
-------
Java is an object-oriented language.

If you return only a string,

text = "Java is an object-oriented language."

Later, if the AI answers

Java is an object-oriented language.

You cannot answer questions like
Which PDF?
Which page?
Which chapter?
Which website?
Which document?
because that information is lost.



What is a Document?

LangChain introduces a class called Document.

Think of it like a small container.

Instead of storing only text,
it stores
    ->the text
    ->extra information about the text

    
A Document contains:
    ->page_content
    ->metadata

"""



from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path




class DocumentLoader:
    def load(self, file_path: str):
        loader = PyPDFLoader(file_path)
        return loader.load()
    



# loader=DocumentLoader()
# docs=loader.load("../../data/java_introduction.pdf")
# for i, doc in enumerate(docs, start=1):
#     print("=" * 80)
#     print(f"Document {i}")
#     print(f"Page: {doc.metadata['page'] + 1}")
#     print(f"Source: {doc.metadata['source']}")
#     print("-" * 80)
#     print(doc.page_content)
#     print()











'''

What happens internally?
Java.pdf

↓

PyPDFLoader

↓

Page 1

↓

Document

↓

Page 2

↓

Document

↓

Page 3

↓

Document

If your PDF has 100 pages,
    you'll receive:-> list[Document]


Why One Document Per Page?
    Because later we'll split each page into chunks.
    If we read the entire PDF as one giant string,
    chunking becomes less accurate.
'''