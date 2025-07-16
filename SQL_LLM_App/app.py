from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

import streamlit as st
import os
import sqlite3

import google.generativeai as genai

# Configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load google gemini model and sql provide query as response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([prompt[0], question])
    return response.text


## Function to retrieve query from the sql database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

## Define the prompt
prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS,
    SECTION and MARKS\n\nExample 1 - How many entries of records are present?,
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT;
    \nExample 2 - Tell me all the students studying in Data Science class?,
    the SQL command will be something like this SELECT * FROM STUDENT where CLASS="DATA SCIENCE";
    also the sql code should not have ``` in beginning or end and sql word in the output
    """
]

## Streamlit UI
st.set_page_config(page_title="Retrieve any SQL Query", page_icon=":tada:")
st.title("SQL Query Generator")

question = st.text_input("Enter your question", key="input")

submit = st.button("Submit")

if submit:
    response = get_gemini_response(question, prompt)
    print(response)
    data = read_sql_query(response, "student.db")
    st.subheader("The response is")
    for row in data:
        print(row)
        st.header(row)