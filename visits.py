import sqlite3
from validation import get_valid_date

DATABASE = "ehr.db"


def add_visit():
    patient_id = input("Enter patient_id: ")
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM patients WHERE patient_id = ?", (patient_id,))
    patient = cursor.fetchone()
    
    if not patient:
        print("Patient not found.")
        conn.close()
        return
    
    visit_date = geet_valid_date("Visit date (YYYY-MM-DD): ")
    provider = input("Provider Name: ")
    reason = input("Reason for visit: ")
    notes = input("Visit notes: ")
    
    cursor.execute("""
                    INSERT INTO visits(
                    patient_id,
                    visit_date,
                    provider,
                    reason,
                    notes
                    )
                    
                    VALUES (?, ?, ?, ?, ?)
                    """,
                           (patient_id,
                          visit_date,
                          provider,
                          reason,
                          notes
                          ))
    conn.commit()
    conn.close()
    
    print("Visit added successfully.")
    
def show_patient_visits():
    patient_id = input("Enter patient_id: ")
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute("""
                    SELECT * FROM visits where patient_id = ?""", (patient_id,))
    
    visits = cursor.fetchall()
    conn.close()
    
    if not visits:
        print("No visits found for this patient.")
        return
    
    print("\n---PATIENTS VISITS---")
    
    for visit in visits:
        print(
            f"Visit Id: {visit[0]} |"
            f"Date: {visit[1]} |"
            f"Provider: {visit[2]} |"
            f"Reason: {visit[3]} |"
            f"Notes: {visit[4]}"
            )
    

    
    