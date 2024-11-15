# FHIR Query Generator

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
