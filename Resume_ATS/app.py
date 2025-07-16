from dotenv import load_dotenv
load_dotenv()  # loads environment variables from .env file

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
import pdf2image
import io
import base64

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.txt

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": img_byte_arr
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No PDF file uploaded.")

## Streamlit App

st.set_page_config(page_title="Resume ATS")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload Your Resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF File uploaded successfully.")

submit1 = st.button("Tell Me About the resume")

# submit2 = st.button("How can I improvise my skills")

submit3 = st.button("Percentage Match")

input_prompt1 = """
You are an experienced Techinical Human Resource Manager, your task is to review the provided resume 
against the job description.
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and weakness of the applicant in relation to the specified job description.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of Data Science,
Web development, Big Data Engineering, DEVOPS,Data Analyst and deep ATS functionality,
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches 
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("No PDF file uploaded.")
elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("No PDF file uploaded.")