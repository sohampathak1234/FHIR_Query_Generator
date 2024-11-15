# FHIR Query Generator 🔥

The **FHIR Query Generator** project allows users to generate SQL queries from natural language inputs to interact with a PostgreSQL database. It is designed to work with FHIR-compliant NDJSON medical records, enabling efficient data processing, querying, and visualization.

## Features

- **FHIR Data Parsing**: Parses and imports FHIR-compliant NDJSON data into a PostgreSQL database.
- **Natural Language to SQL**: Converts natural language queries into SQL commands using a language model.
- **Database Querying**: Executes generated SQL queries and returns results.
- **Frontend Interface**: Provides an intuitive interface for users to input queries and view results.

## Project Structure

- `app.py`: Backend logic for processing natural language queries and generating SQL.
- `frontend.py`: Frontend logic for user interaction and result visualization.
- `parse.py`: Script for importing FHIR NDJSON data into the PostgreSQL database.
- `medical_record_fhir.json`: Example file containing FHIR-compliant patient data.

## Requirements

- Python 3.8+
- PostgreSQL
- Required Python packages (see `requirements.txt`)

## Setup Instructions

1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/fhir-query-generator.git
   cd fhir-query-generator

2. Install Dependencies
    ```bash
    pip install -r requirements.txt

3. Set Up PostgreSQL

    1. Create a new PostgreSQL database:
    ```sql
    CREATE DATABASE MedicalRecord;
    ```

    2. Create a user and grant permissions:
    ```sql
    CREATE USER fhir_user WITH PASSWORD 'yourpassword';
    GRANT ALL PRIVILEGES ON DATABASE MedicalRecord TO fhir_user;
    ```

    3. Update the connection details in app.py and parse.py.

    4. Import FHIR Data
    Run the parsing script to populate the database:
    ```bash
    python parse.py --file medical_record_fhir.json
    ```

    OR

    Import MedicalRecord.sql into PostgreSQL

4. Start the Application

    Start the Backend:
    ```bash
    python app.py
   ```
    Start the Frontend:
    ```bash
    streamlit run frontend.py
   ```

