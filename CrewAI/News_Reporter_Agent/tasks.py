from crewai import Task
from tools import tool
from agents import researcher, news_writer

# Research Task
research_task = Task(
    description=(
        "Identify the next big trend in {topic}."
        "Focus on identifying pros and cons and the overall narrative."
        "Your final report should clearly articulate the key points,"
        "its market opportunities, and potential risks."
    ),
    expected_output="A comprehensive 3 paragraph long report on the latest AI trends.",
    tools=[tool],
    agent=researcher
)

# Writing Task with language model configuration
write_task = Task(
    description=(
        "Write a compelling news article about the latest advancements in {topic}."
        "The article should be engaging, informative, and accessible to a general audience."
        "Ensure to include key insights from the research conducted by the Senior Researcher agent."
    ),
    expected_output="A well-structured news article that highlights the latest advancements in AI.",
    tools=[tool],
    agent=news_writer
)