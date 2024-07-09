import os
from crewai import Agent, Task, Crew
from dotenv import load_dotenv
load_dotenv()
from tools import *



from langchain_google_genai import ChatGoogleGenerativeAI


gemini_llm=ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", 
    verbose=True, 
    temperature=0.5, 
    google_api_key=os.getenv("GOOGLE_API_KEY")
)



# Create agents
researcher = Agent(
    role='Agricultural Research Expert',
    goal='Provide latest and concise information of external conditions like pH of nutrient solution, EC of nutrient solution, Optimal temperature, Humidity at different stages of hydroponic farming of {topic}',
    backstory=('An expert agruculturist and research '
                'scientist in the field of agriculture '
                'and hydroponics'),
    verbose=True, 
    llm=gemini_llm,
    allow_delegation=True, 
    max_iterations=5,
    memory=True, 
    tools=[search_tool, web_rag_tool]

)

text_miner = Agent(
    role='Text Mining Specialists',
    goal="Ouptut a json file having keys 'current plant', 'number of days from seeding', 'pH' of the nutrient solution, 'EC of the nutrient solution', 'optimal temperature required', 'optimal humidity' with 'number of days from seeding' values should be at intervals of 7, from seeding to harvesting in hydroponic farming of {topic} plant. The final json file should have objects with  'number of days from seeding' at regular intervals of 7 till harvesting day.",
    backstory="A skilled text miner who can extract critical information like pH, EC, optimal temperature, optimal humidity of growing {topic} hydropincally  from different resources",
    verbose=True, 
    llm=gemini_llm, 
    max_iterations=20,
    memory=True, 
    tools = [file_tool, docs_tool, search_tool], 
    allow_delegation=False, 
    output_json=True

    
)