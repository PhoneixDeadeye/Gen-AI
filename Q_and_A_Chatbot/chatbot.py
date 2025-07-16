from dotenv import load_dotenv
load_dotenv()  # loads environment variables from .env file

import streamlit as st
import os
import google.generativeai as genai

# Configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(history=[])

# Function to get response from Gemini
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    full_response = ""

    for chunk in response:
        if chunk.text:
            full_response += chunk.text
    return full_response

# Initialize Streamlit app
st.set_page_config(page_title="Q&A Chatbot")
st.header("Gemini Q&A Chatbot")

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Get input from user
input = st.text_input("Input: ", placeholder="Type your question here...", key="input")
submit = st.button("Ask the question")

if submit and input:
    response = get_gemini_response(input)

    # Add question and response to chat history
    st.session_state.chat_history.append(("question", input))
    st.session_state.chat_history.append(("response", response))

    # Display response
    st.subheader("The response is:")
    st.write(response)

# Display chat history
st.subheader("Chat History:")
for role, text in st.session_state.chat_history:
    st.write(f"**{role.capitalize()}**: {text}")
