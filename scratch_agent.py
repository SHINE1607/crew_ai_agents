import os
from crewai import Agent, Task, Crew
from dotenv import load_dotenv
load_dotenv()
# Importing crewAI tools
from crewai_tools import (
    DirectoryReadTool,
    FileReadTool,
    SerperDevTool,
    WebsiteSearchTool
)


from langchain_google_genai import ChatGoogleGenerativeAI


gemini_llm=ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", 
    verbose=True, 
    temperature=0.5, 
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# customizing webragtool to gemini model

# Instantiate tools
docs_tool = DirectoryReadTool(directory='./blog-posts')
file_tool = FileReadTool()
search_tool = SerperDevTool()
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

# Create agents
researcher = Agent(
    role='Market Research Analyst',
    goal='Provide up-to-date market analysis of the AI industry',
    backstory='An expert analyst with a keen eye for market trends.',
    tools=[search_tool, web_rag_tool],
    verbose=True, 
    llm=gemini_llm,
    max_iter=15
)

writer = Agent(
    role='Content Writer',
    goal='Craft engaging blog posts about the AI industry',
    backstory='A skilled writer with a passion for technology.',
    tools=[docs_tool, file_tool],
    verbose=True, 
    llm=gemini_llm, 
    max_execution_time=60,
    max_iteration=15

    
)

# Define tasks
research = Task(
    description='Research the latest trends in the AI industry and provide a summary.',
    expected_output='A summary of the top 3 trending developments in the AI industry with a unique perspective on their significance.',
    agent=researcher
)

write = Task(
    description='Write an engaging blog post about the AI industry, based on the research analyst’s summary. Draw inspiration from the latest blog posts in the directory.',
    expected_output='A 4-paragraph blog post formatted in markdown with engaging, informative, and accessible content, avoiding complex jargon.',
    agent=writer,
    output_file='blog-posts/new_post.md'  # The final blog post will be saved here
)

# Assemble a crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research, write],
    verbose=2
)

# Execute tasks
crew.kickoff()