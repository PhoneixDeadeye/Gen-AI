from dotenv import load_dotenv
load_dotenv()  # loads environment variables from .env file

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Set up Google Generative AI API key
api_key = os.getenv("GOOGLE_GENERATIVE_AI_API_KEY")

## Function to load Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type, # Get the MIME type of the uploaded file
                "data": bytes_data  # Use the bytes data directly 
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No image file uploaded.")

## Initializing Streamlit app
st.set_page_config(page_title="Multi-Language Invoice Extractor")

st.header("Multi-Language Invoice Extractor")

input = st.text_input("Input Prompt: ", placeholder="Type your question here...", key="input")
uploaded_file = st.file_uploader("Choose an image of the invoice...", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Invoice", use_container_width=True)

submit = st.button("Tell me about this invoice")

input_prompt = """
You are an expert in understanding invoices. We will upload an image as invoice
and you will have to answer any questions based on 
the uploaded invoice image.
"""

# If submit button is pressed
if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("The Response is")
    st.write(response)