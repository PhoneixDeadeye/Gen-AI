from crewai import Agent
from crewai import LLM
from custom_tools import yt_tool

from dotenv import load_dotenv

load_dotenv()

import os
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")
os.environ["GEMINI_MODEL_NAME"] = "gemini-1.5-flash"

gemini_llm = LLM(
    model="gemini/gemini-1.5-flash",  # or "gemini/gemini-pro" if you want
    api_key=os.getenv("GEMINI_API_KEY")
)
## Create a senior blog content researcher

blog_researcher = Agent(
    role = 'Blog Researcher from YouTube videos',
    goal = 'Get the relevant video content for the topic {topic} from YouTube channel',
    verbose = True,
    memory = True,
    backstory=(
        "Expert in understanding videos in AI Data Science, Machine Learning and Gen AI and providing suggestion"
    ),
    tools=[yt_tool],
    
    allow_delegation = True,
    llm=gemini_llm
)

## Creating a senior blog writer agent with YT Tool

blog_writer = Agent(
    role = 'Blog Writer from YouTube videos',
    goal = 'Narrate compelling tech stories about the video {topic} from YT channel',
    verbose = True,
    memory = True,
    backstory=(
        "With a flair for simplifying complex topics, you craft"
        "engaging narratives that captivate and educate, bringing new"
        "discoveries to light in an accessible manner."
    ),
    tools=[yt_tool],
    allow_delegation = False,
    llm=gemini_llm
)

