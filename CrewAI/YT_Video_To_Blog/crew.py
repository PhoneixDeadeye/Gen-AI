import sys
sys.stdout.reconfigure(encoding='utf-8')
from crewai import Crew, Process
from agents import blog_writer, blog_researcher, gemini_llm
from custom_tools import yt_tool
from tasks import write_task, research_task
import os

crew = Crew(
    agents = [blog_writer, blog_researcher],
    tasks = [research_task, write_task],
    process = Process.sequential,
    memory = True,
    cache = True,
    max_rpm = 100,
    share_crew = True,
    llm = gemini_llm,
    embedder={
        "provider": "google",
        "config": {
            "model": "models/embedding-001",
            "api_key": os.getenv("GEMINI_API_KEY")
        }
    }
)

## Start the task execution
result = crew.kickoff(inputs={'youtube_video_url': 'https://www.youtube.com/watch?v=88yQTzlmsiA'})
print(result)