import sqlite3

from validation import (get_valid_name,
                        get_valid_dob,
                        get_valid_sex,
                        get_valid_phone,
                        get_valid_medical_text)

from visits import add_visit, show_patient_visits

DATABASE = "ehr.db"

def register_patient():
    print("\n ---REGISTER NEW PATIENT---")
    
    first_name = get_valid_name("First name: ")
    last_name = get_valid_name("Last name: ")
    dob = get_valid_dob()
    sex = get_valid_sex()
    phone = get_valid_phone()
    address = input("Address: ")
    emergency_contact = get_valid_phone()
    condition = get_valid_medical_text("Current Condition")
    allergies = get_valid_medical_text("Allergies: ")
    
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
                    phone,
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
            f"Phone: {patient[5]}"
            f"Condition: {patient[6]} |"
            f"Allergies: {patient[7]} |"
            )
def find_patients():
    patient_id = int(input("Enter patient Id: "))
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute(
                "SELECT * FROM patients WHERE patient_id = ?", (patient_id,)
                )
    patient = cursor.fetchone()
    conn.close()
    
    if patient:
        print("\n---Patient Found---")
        print(patient)
        
    else:
        print("Patient not found.")

def update_patient():
    patient_id = int(input("Enter patient ID: "))
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM patients where patient_id = ?", (patient_id,))
    
    patient = cursor.fetchone()
    
    if not patient:
        print("Patient nof found.")
        conn.close()
        return
    
    print("\n---UPDATE PATIENT---")
    phone = input("Enter New phone number: ")
    address = input("Enter New address: ")
    condition = input("New condition: ")
    allergies = input("New Allergies: ")
    
    cursor.execute("""
                    UPDATE patients
                    SET phone = ?,
                        address = ?,
                        condition = ?,
                        allergies = ?
                    WHERE patient_id = ?
                    """, (
                        phone, address, condition, allergies, patient_id
                        ))
    conn.commit()
    conn.close()
    print("Patient Updated Successfully.")
      
def del_patient():
    patient_id = input("Enter patient id: ")
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute(
                    "SELECT * FROM patients WHERE patient_id = ?", (patient_id,))

    patient = cursor.fetchone()
    
    if not patient:
        print("Patient not found.")
        conn.close()
        return
    
    print("\nPatient Found.")
    print(patient)
    
    confirm = input("Are you sure you want to delete this patient? (y/n): ").strip().lower()
    if confirm == "y":
        cursor.execute("DELETE FROM patients WHERE patient_id = ?", (patient_id,))
        
        conn.commit()
        print("Patient Deleted Successfully.")
        
    else:
        print("Delete Cancelled.")
    conn.close()
        

while True:
    print("\n---PATIENT MENU---")
    print("1. Register a new patient")
    print("2. Show Patients")
    print("3. Find Patients")
    print("4. Update Patient")
    print("5. Delete Patient")
    print("6. Add Visit")
    print("7. Show Patient Visits")
    print("8. Exit")
    
    choice = int(input("Choose an option: "))
    if choice == 1:
        print("CHOICE:", choice)
        print("TYPE:", type(choice))
        register_patient()
        
    elif choice == 2:
        show_patients()
        
    elif choice == 3:
        find_patients()
        
    elif choice == 4:
        update_patient()
        
    elif choice == 5:
        del_patient()
        
    elif choice == 6:
        add_visit()
        
    elif choice == 7:
        show_patient_visits()
    
    elif choice == 8:
        print("Exiting Patient System.")
        break
    
    else:
        print("invalid Choice.")
        
        

        