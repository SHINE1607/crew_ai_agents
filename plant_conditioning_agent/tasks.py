from tools import (
    docs_tool, 
    file_tool, 
    search_tool, 
    web_rag_tool, 
    webscraping_tool, 
    pdf_search_tool
)
from crewai import Agent, Task, Crew
from agents import researcher, text_miner
from dotenv import load_dotenv
import os
load_dotenv()
plant = os.environ["topic"]
# Define tasks
research_task = Task(
    description= (
        "To research and aggregate the most relevant and concise documented information "
        "about end to end growing of the {topic} hydroponically at different stages of growth"
    ),
    expected_output='A comprehensive article on how to grow {topic} hydroponically',
    agent=researcher, 
    tools=[search_tool, webscraping_tool]
    
)

json_writer_task= Task(
    description="To extract various information like 'number of days from seeding', 'pH of the nutrient solution', 'EC of the nutrient solution', 'optimal temperature required', 'optimal humidity' of this growing {topic} hydroponically from the research summary at  intervals of 7, from seeding to harvesting.",
    expected_output="A json file having keys 'current plant', 'number of days from seeding', 'pH' of the nutrient solution, 'EC of the nutrient solution', 'optimal temperature required', 'optimal humidity', 'light intensity'. With 'number of days from seeding' values should be at intervals of 7, from seeding to harvesting",
    agent=text_miner,
    output_file=f'ouptut/{plant}.json',  # The final blog post will be saved here
    context=[research_task], 
    tools=[docs_tool, file_tool],
    async_execution=False,
)



