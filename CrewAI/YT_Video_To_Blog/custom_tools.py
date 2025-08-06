# custom_tools.py

import os
import requests
import google.generativeai as genai
from dotenv import load_dotenv
from langchain.tools import tool
from crewai.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from crewai_tools import YoutubeVideoSearchTool
# Load environment variables from .env file
load_dotenv()
import os

youtube_search_tool = YoutubeVideoSearchTool(
    config={
        "embedder": {
            "provider": "google",
            "config": {
                "model": "models/embedding-001",
                "google_api_key": os.getenv("GEMINI_API_KEY")
            }
        }
    }
)

