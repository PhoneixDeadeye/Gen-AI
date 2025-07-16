import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini response function
def get_gemini_response(prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

# Extract text from uploaded PDF
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

# Prompt Template
input_prompt = """
You are an experienced ATS (Applicant Tracking System) evaluator skilled in software engineering, machine learning, data science, and big data domains.

Evaluate the following resume against the job description.

Provide:
1. A JD Match percentage (how well the resume matches the JD).
2. A list of Missing Keywords the resume lacks based on the JD.
3. A Profile Summary — helpful suggestions on improving the resume.

Return ONLY in this valid JSON format:
{{
  "JD Match": "XX%",
  "MissingKeywords": ["keyword1", "keyword2", ...],
  "Profile Summary": "..."
}}

Resume:
{text}

Job Description:
{jd}
"""

# Streamlit App UI
st.title("🤖 Smart ATS Resume Evaluator")
st.markdown("Upload your resume and paste the job description to check ATS compatibility.")

jd = st.text_area("📋 Paste the Job Description", height=250)
uploaded_file = st.file_uploader("📎 Upload Your Resume (PDF)", type=["pdf"], help="Only PDF files allowed")

submit = st.button("🔍 Evaluate Resume")

if submit:
    if uploaded_file is not None and jd.strip() != "":
        with st.spinner("Analyzing resume..."):
            # Extract resume text
            text = input_pdf_text(uploaded_file)

            # Format the final prompt
            final_prompt = input_prompt.format(text=text, jd=jd)

            # Get Gemini's structured response
            try:
                raw_response = get_gemini_response(final_prompt)
                parsed = json.loads(raw_response)

                st.success("✅ Analysis Complete!")
                st.subheader("📊 JD Match")
                st.write(parsed.get("JD Match", "Not found"))

                st.subheader("❌ Missing Keywords")
                st.write(parsed.get("MissingKeywords", []))

                st.subheader("📝 Profile Summary")
                st.write(parsed.get("Profile Summary", "Not available"))

            except Exception as e:
                st.error("❌ Failed to parse Gemini response.")
                st.text("Raw response:")
                st.text(raw_response)
                st.exception(e)
    else:
        st.warning("Please upload a PDF resume and paste the job description.")