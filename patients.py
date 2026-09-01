import sqlite3

DATABASE = "ehr.db"

def register_patient():
    print("\n ---REGISTER NEW PATIENT---")
    
    first_name = input("First name: ")
    last_name = input("Last name: ")
    dob = input("date of birth(YYYY-MM-DD): ")
    sex = input("Sex: ")
    phone = input("Phone number: ")
    address = input("Address: ")
    emergency_contact = input("Emergency contact number: ")
    condition = input("Current condition: ")
    allergies = input("Allergies: ")
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute("""
                   INSERT INTO patients(
                   first_name,
                   last_name,
                   dob,
                   sex,
                   phone,
                   address,
                   emergency_contact,
                   condition,
                   allergies
                   )
                   VALUES(?,?,?,?,?,?,?,?,?)
                    """, (
                    first_name,
                   last_name,
                   dob,
                   sex,
                   phone,
                   address,
                   emergency_contact,
                   condition,
                   allergies
                        ))
    
    
    conn.commit()
    
    patient_id = cursor.lastrowid
    conn.close()
    
    print("\nPatient registered successfully. ")
    print("Patient ID:", patient_id)


def show_patients():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute("""
                    SELECT patient_id,
                    first_name,
                    last_name,
                    dob,
                    sex,
                    condition,
                    allergies
                    FROM patients
                    """)
    
    patients = cursor.fetchall()
    print("Debug:", patients)
    conn.close()
    
    
    print("\n---PATIENT LIST---")
    
    if not patients:
        print("Patients Not Found. ")
        return
    
    for patient in patients:
        print(
            f"ID: {patient[0]} | "
            f"Name: {patient[1]} {patient[2]} | "
            f"DOB : {patient[3]} | "
            f"Sex: {patient[4]} | "
            f"Condition: {patient[5]} |"
            f"Allergies: {patient[6]} |"
            )

while True:
    print("\n---PATIENT MENU---")
    print("1. Register a new patient")
    print("2. Show Patients")
    print("3. Exit")
    
    choice = int(input("Choose an option: "))
    if choice == 1:
        register_patient()
        
    elif choice == 2:
        show_patients()
        
    elif choice == 3:
        print("Exiting Patient System.")
        break
    else:
        print("invalid Choice.")
        
        
        
        
        