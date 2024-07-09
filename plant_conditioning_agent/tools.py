import os
from crewai_tools import (
    DirectoryReadTool,
    FileReadTool,
    SerperDevTool,
    WebsiteSearchTool, 
    ScrapeWebsiteTool, 
    PDFSearchTool
)


docs_tool = DirectoryReadTool(directory='./output')
file_tool = FileReadTool()
search_tool = SerperDevTool()
webscraping_tool = ScrapeWebsiteTool()

pdf_search_tool = PDFSearchTool(
    config=dict(
        llm=dict(
            provider="google", # or google, openai, anthropic, llama2, ...
            config=dict(
                model="gemini-1.5-flash",
                # temperature=0.5,
                # top_p=1,
                # stream=true,
            ),
        ),
        embedder=dict(
            provider="google", # or openai, ollama, ...
            config=dict(
                model="models/embedding-001",
                task_type="retrieval_document",
                # title="Embeddings",
            ),
        ),
    )
)
web_rag_tool = WebsiteSearchTool(
    config=dict(
        llm=dict(
            provider="google", 
            config=dict(
                model="gemini-1.5-flash",
            ),
        ),
        embedder=dict(
            provider="google", # or openai, ollama, ...
            config=dict(
                model="models/embedding-001",
                task_type="retrieval_document",
                # title="Embeddings",
            ),
        ),
    )
)