import psycopg2
import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq

# Initialize FastAPI app and Groq client
app = FastAPI()
client = Groq(api_key="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")

# Function to establish connection to the PostgreSQL database
def connect_to_db():
    return psycopg2.connect(
        dbname="MedicalRecord",
        user="postgres",
        password="password",
        host="localhost",
        port="5432"
    )

# Data model for the question input using Pydantic
class QuestionRequest(BaseModel):
    question: str

# Data model for SQL execution input using Pydantic
class SQLRequest(BaseModel):
    sql_query: str


# Helper function to create a prompt for the LLM
def create_sql_prompt(question):
    schema_description = (    ## Description of the database schema for the language model
       "The database schema includes the following tables:\n"
        "- Patient: Contains patient information, with fields such as id, name, family_name, given_name, gender, "
        "birth_date, telecom_email, telecom_sms, address_text, address_city, address_state, address_postal_code and address_country.\n"
        "- Medication: Records information about medications with fields such as id, code, form_code, dose, and frequency.\n"
        "- Condition: Logs patient conditions, including fields like id, identifier_value, clinical_status_code, "
        "verification_status_code, code, subject_reference (FK to Patient), and onset_datetime.\n"
        "- Observation: Stores observations like blood pressure with fields such as id, status, category_code, code, "
        "subject_reference (FK to Patient), effective_datetime, systolic_blood_pressure, and diastolic_blood_pressure.\n"
        "- CarePlan: Includes patient care plans with fields such as id, title, description, status, intent, and "
        "subject_reference (FK to Patient).\n"
        "- BodyStructure: Contains information about body structures with fields like id, identifier_value, morphology_code, "
        "morphology_text, location_code, location_text, description, and patient_reference (FK to Patient).\n"
        "The database is FHIR Compliant"
        "Use this schema to generate the PostGreSQL query in response to the question."
    )
    return f"{schema_description}\n\nQuestion: '{question}'\nPlease output only the SQL query." #Combine schema and question into a single prompt

# Helper function to extract SQL query from the language model response
def extract_sql_query(response_text):
     # Regex to match SQL statements
    match = re.search(r"(SELECT|INSERT|UPDATE|DELETE|WITH|CREATE|DROP|ALTER)\s.*;", response_text, re.IGNORECASE | re.DOTALL)
    return match.group(0).strip() if match else None

# Route to generate SQL query
@app.post("/generate_sql")
async def generate_sql(request: QuestionRequest):
    prompt = create_sql_prompt(request.question)
    response = client.chat.completions.create( ## Send the prompt to the language model via Groq API
        model="llama3-8b-8192",    ## Model to use
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2     # Temperature for model response
    )
    response_text = response.choices[0].message.content    # Extract the response content
    sql_query = extract_sql_query(response_text)           # Extract the SQL query from the response
    if not sql_query:
        raise HTTPException(status_code=400, detail="Failed to generate SQL query.")
    return {"sql_query": sql_query}

# Route to execute SQL query
@app.post("/execute_query")
async def execute_query(request: SQLRequest):
    connection = connect_to_db()    # Connect to the PostgreSQL database
    cursor = connection.cursor()
    try:
        cursor.execute(request.sql_query)
        rows = cursor.fetchall()                                   # Fetch all rows from the executed query
        column_names = [desc[0] for desc in cursor.description]    # Get column names from the cursor description
        result = [dict(zip(column_names, row)) for row in rows]    # Combine column names and row data into a dictionary
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing SQL: {str(e)}")
    finally:    
        cursor.close()
        connection.close()     # Ensure database connection is closed
    return {"results": result}    ## Return the query results as a JSON response
