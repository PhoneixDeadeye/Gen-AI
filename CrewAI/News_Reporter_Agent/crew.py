from crewai import Crew
from agents import researcher, news_writer
from tasks import research_task, write_task

## Forming the tech focused crew with some enhanced configurations
crew = Crew(
    agents=[researcher, news_writer],
    tasks=[research_task, write_task],
    verbose=True,
    planning=True,  # Enable planning feature
)

# Execute tasks
result = crew.kickoff()
print(result)