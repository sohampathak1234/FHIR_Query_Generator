# frontend.py
import streamlit as st
import requests
import pandas as pd

# Base URL of the FastAPI server
BASE_URL = "http://localhost:8000"

st.title("FHIR Medical Database of 200 Patients")
st.write("Ask questions about the patients, and get results directly!")

# Function to interact with the generate_sql API endpoint
def generate_sql(question):
    response = requests.post(f"{BASE_URL}/generate_sql", json={"question": question})
    if response.status_code == 200:
        return response.json().get("sql_query")
    else:
        st.error("Failed to generate SQL query.")
        return None

# Function to interact with the execute_query API endpoint
def execute_query(sql_query):
    response = requests.post(f"{BASE_URL}/execute_query", json={"sql_query": sql_query})
    if response.status_code == 200:
        return response.json().get("results")
    else:
        st.error("Failed to execute SQL query.")
        return None

# User input in Streamlit
question = st.text_input("Enter your question:")
if st.button("Submit"):
    if question:
        sql_query = generate_sql(question)
        if sql_query:
            st.write("Generated SQL Query:", sql_query)
            results = execute_query(sql_query)
            if results:
                df = pd.DataFrame(results)
                st.write("Query Results:")
                st.dataframe(df)
            else:
                st.warning("No results found.")
    else:
        st.warning("Please enter a question.")
