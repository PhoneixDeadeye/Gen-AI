from dotenv import load_dotenv
load_dotenv() ## loads environment variables from .env file

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Gemini pro model and get responses
model = genai.GenerativeModel("gemini-1.5-pro")

def get_gemini_response(input, image):
    if input!="":
        response = model.generate_content([input, image])
    else:    
        response = model.generate_content(image)
        return response.text
    response = model.generate_content(image)
    return response.text

## Initializing Streamlit app

st.set_page_config(page_title="Image Demo")

st.header("Gemini Image Application")

input = st.text_input("Input: ", placeholder="Type your question here...", key="input")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_container_width=True)

submit = st.button("Tell me about this image")

## If submit button is clicked
if submit:
    response = get_gemini_response(input, image)
    st.subheader("Response:")
    st.write(response)