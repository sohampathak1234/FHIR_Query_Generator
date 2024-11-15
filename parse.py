import json
import psycopg2
from psycopg2 import sql

# Database connection setup
conn = psycopg2.connect(
    dbname="MedicalRecord",
    user="postgres",
    password="password",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Load the JSON data
file_path = 'medical_record_fhir.json'
with open(file_path, 'r') as f:
    data = json.load(f)

# Insert data into PostgreSQL tables
for patient in data["patients"]:
    # Insert into Patient table
    patient_id = patient["id"]
    cur.execute("""
        INSERT INTO Patient (id, name, family_name, given_name, gender, birth_date, telecom_email, telecom_sms, address_text, address_city, address_state, address_postal_code, address_country)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (patient_id, patient["name"]["family"], patient["name"]["family"], patient["name"]["given"][0], patient["gender"], patient["birthDate"],
         patient["telecom"][1]["value"], patient["telecom"][0]["value"], patient["address"]["line"][0], patient["address"]["city"],
         patient["address"]["state"], patient["address"]["postalCode"], patient["address"]["country"])
    )

    # Insert into Condition table
    for condition in patient["conditions"]:
        cur.execute("""
            INSERT INTO Condition (id, identifier_value, clinical_status_code, verification_status_code, code, subject_reference, onset_datetime)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (condition["id"], condition["id"], condition["clinicalStatus"], condition["verificationStatus"], condition["code"]["text"],
             patient_id, condition["onsetDateTime"])
        )

    # Insert into Observation table
    for observation in patient["observations"]:
        systolic = observation["component"][0]["valueQuantity"]
        diastolic = observation["component"][1]["valueQuantity"]
        cur.execute("""
            INSERT INTO Observation (id, status, category_code, code, subject_reference, effective_datetime, systolic_blood_pressure, diastolic_blood_pressure)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (observation["id"], observation["status"], "vital-signs", "Blood Pressure", patient_id,
             observation["effectiveDateTime"], systolic, diastolic)
        )

    # Insert into Medication table
    for medication in patient["medications"]:
        cur.execute("""
            INSERT INTO Medication (id, code, form_code, dose, frequency)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (medication["id"], medication["code"]["text"], medication["form"], medication["dose"], medication["frequency"])
        )

    # Insert into CarePlan table
    for care_plan in patient["carePlan"]:
        cur.execute("""
            INSERT INTO CarePlan (id, title, description, status, intent, subject_reference)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (care_plan["id"], care_plan["title"], care_plan["description"], care_plan["status"], care_plan["intent"], patient_id)
        )

    # Insert into BodyStructure table
    for body_structure in patient.get("bodyStructure", []):
        cur.execute("""
            INSERT INTO BodyStructure (id, identifier_value, morphology_code, morphology_text, location_code, location_text, description, patient_reference)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (body_structure["id"], body_structure["identifier"]["value"], 
             body_structure["morphology"]["coding"][0]["code"], body_structure["morphology"]["coding"][0]["display"],
             body_structure["location"]["coding"][0]["code"], body_structure["location"]["coding"][0]["display"],
             body_structure["description"], patient_id)
        )

# Commit changes and close the connection
conn.commit()
cur.close()
conn.close()
