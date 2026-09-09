import sqlite3

from validation import get_valid_date

from pulse_sensor import get_heart_rate


DATABASE = "ehr.db"


def add_vitals():
    patient_id = input("Enter patient id: ")
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute(
                "SELECT * FROM patients WHERE patient_id = ?", (patient_id,)
                )
    patient = cursor.fetchone()
    
    if not patient:
        print("Patient not found.")
        conn.close()
        return
    
    measurement_date = get_valid_date("Measurement date (YYYYMMDD):")
    #systolic_bp = int(input("Systolic BP: "))
    #diastolic_bp = int(input("Diastolic BP: "))
    heart_rate = get_heart_rate()
    if heart_rate is None:
        print("Heart rate measurement faild.")
        return
    
    #temperature = float(input("Temperature: "))
    #weight = float(input("Weight in kg: "))
    #height = float(input("Height in meters: "))
    
    #bmi = weight / (height**2)
    
    cursor.execute("""
    INSERT INTO vitals (
        patient_id,
        measurement_date,
        heart_rate
    )
    VALUES (?, ?, ?)
""", (
    patient_id,
    measurement_date,
    heart_rate
))
    
    conn.commit()
    conn.close()

    print("Vitals added successfully.")
    print("Heart rate:", heart_rate, "BPM")

add_vitals()

    
    
    
    