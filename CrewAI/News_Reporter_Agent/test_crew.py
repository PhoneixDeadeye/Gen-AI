from crewai import Crew, Process, Agent, Task
from crewai.tools import tool

# Create a simple mock LLM
class MockLLM:
    def invoke(self, messages):
        return "This is a mock response for testing purposes."

# Create a simple search tool
@tool
def search_web(query: str) -> str:
    """Search the web for information"""
    return f"Mock search result for: {query}"

# Create agents
researcher = Agent(
    role="Senior Researcher",
    goal="Uncover groundbreaking technologies in {topic}",
    verbose=True,
    backstory="Driven by curiosity, you're at the forefront of innovation.",
    tools=[search_web],
    llm=MockLLM(),
    allow_delegation=True,
)

news_writer = Agent(
    role="Writer",
    goal="Narrate compelling tech stories about {topic}",
    verbose=True,
    backstory="With a flair for simplifying complex topics, you craft engaging narratives.",
    tools=[search_web],
    llm=MockLLM(),
    allow_delegation=True
)

# Create tasks
research_task = Task(
    description="Identify the next big trend in {topic}. Focus on identifying pros and cons.",
    expected_output="A comprehensive report on the latest AI trends.",
    tools=[search_web],
    agent=researcher
)

write_task = Task(
    description="Write a compelling news article about the latest advancements in {topic}.",
    expected_output="A well-structured news article that highlights the latest advancements in AI.",
    tools=[search_web],
    agent=news_writer
)

# Create crew
crew = Crew(
    agents=[researcher, news_writer],
    tasks=[research_task, write_task],
    process=Process.sequential,
)

# Run the crew
result = crew.kickoff(inputs={'topic': 'Artificial Intelligence in healthcare'})
print(result) 