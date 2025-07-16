from dotenv import load_dotenv
load_dotenv() ## loads environment variables from .env file

import streamlit as st
import os
import google.generativeai as genai


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Gemini pro model and get responses
model = genai.GenerativeModel("gemini-1.5-pro")

def get_gemini_response(question):
    response = model.generate_content(question)
    return response.text

## Initializing Streamlit app

st.set_page_config(page_title="Q&A Demo")

st.header("Gemini LLM Application")

input = st.text_input("Input: ", placeholder="Type your question here...", key="input")
submit = st.button("Ask the question")

# When submit button is clicked

if submit: 
    response = get_gemini_response(input)
    st.write("Response: ", response)
