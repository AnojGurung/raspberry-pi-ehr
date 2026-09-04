def get_valid_name(prompt):
    while True:
        name = input(prompt).strip()
        
        if name.isalpha():
            return name
        
        print("Invalid name. Use letters only.")
        
        
def get_valid_dob():
    while True:
        dob = input("Date of birth (yyyy-mm-dd): ").strip()
        
        parts = dob.split("-")
        
        if (
            len(parts) == 3
            and len(parts[0]) == 4
            and len(parts[1]) == 2
            and len(parts[2]) == 2
            and all(part.isdigit() for part in parts)
            ):
            return dob
        print("Invalid DOB. Use YYY-MM-DD format with numbers only.")
        
def get_valid_sex():
    while True:
        sex = input("Sex (M/F/Others): ").strip.lower()
        
        if sex in ["m", "f", "others"]:
            return sex
        print("Invalid option. Enter M, F, or Other.")
        
        
def get_valid_phone():
    while True:
        phone = input("Phone number:").strip()
        
        if phone.isdigit() and len(phone) == 10:
            return phone
        print("Invalid phone number. Enter exactly 10 digits.")
        
def get_valid_medical_text(prompt):
    while True:
        value = input(prompt).strip()
        
        if value:
            return value
            
        print("Input cannot be empty.")
        
        
        
        