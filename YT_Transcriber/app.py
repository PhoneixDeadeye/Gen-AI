import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import os

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

from youtube_transcript_api import YouTubeTranscriptApi

prompt = """
You are a helpful assistant. Your task is to take the transcript of a youtube video and provide a summary of the video 
and providing important summary in points within 250 words. The transcript text will be appended here :
"""

## Getting the transcript data from youtube videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("v=")[1]
        ytt_api = YouTubeTranscriptApi()
        fetched_transcript = ytt_api.fetch(video_id)
        
        transcript = ""
        for snippet in fetched_transcript:
            transcript += snippet.text + " "
        return transcript
    except Exception as e:
        raise e


## Getting the summary based on prompt from Google Gemini
def get_gemini_response(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt+transcript_text)
    return response

st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter the youtube video URL")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)

if st.button("Get detailed notes"):
    transcript_text = extract_transcript_details(youtube_link)
    if transcript_text:
        summary = get_gemini_response(transcript_text, prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary.text)
    