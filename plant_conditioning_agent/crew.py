from crewai import Crew,Process
import sys, os
plant = sys.argv[1]

os.environ["topic"] = plant
from tasks import *
from agents import *

## Forming the tech focused crew with some enhanced configuration
crew=Crew(
    # agents=[researcher,text_miner],
    agents=[researcher],
    # tasks=[research_task, json_writer_task],
    tasks=[research_task],
    process=Process.sequential,

)

## starting the task execution process wiht enhanced feedback

result=crew.kickoff(inputs={"topic": plant})
print(research_task.output.raw_output)
print(result)# Execute tasks
