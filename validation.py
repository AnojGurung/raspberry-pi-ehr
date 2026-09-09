from datetime import datetime


def get_valid_name(prompt):
    while True:
        name = input(prompt).strip()
        
        if name.isalpha():
            return name
        
        print("Invalid name. Use letters only.")
        
        
def get_valid_dob():
    while True:
        dob = input("Date of birth (yyyy-mm-dd): ").strip()
        
        try:
            birth_date = datetime.strptime(dob, "%y-%m-%d").date()
            today = datetime.today().date()
            
            if birth_date > today:
                print("Date of birth cannot be in future.")
                continue
            
            if birth_date.year < 1900:
                print("Year is too old. Enter a Valid Year.")
                continue
            
            return dob
        
        except ValueError:
            print("Invalid date. Use a real data in YYYY-MM-DD format.")
            
        
def get_valid_sex():
    while True:
        sex = input("Sex (M/F/Others): ").strip().lower()
        
        if sex in ["m", "f", "others"]:
            return sex
        print("Invalid option. Enter M, F, or Other.")
        
        
def get_valid_phone():
    while True:
        phone = input("Phone number: ").strip()
        
        if phone.isdigit() and len(phone) == 10:
            return phone
        print("Invalid phone number. Enter exactly 10 digits.")
        
def get_valid_medical_text(prompt):
    while True:
        value = input(prompt).strip()
        
        if value:
            return value
            
        print("Input cannot be empty.")
        
def get_valid_date(prompt):
    while True:
        date_text = input(prompt).strip()

        if date_text.isdigit() and len(date_text) == 8:
            date_text = (
                date_text[:4]
                + "-"
                + date_text[4:6]
                + "-"
                + date_text[6:]
            )

        try:
            datetime.strptime(date_text, "%Y-%m-%d").date()
            return date_text

        except ValueError:
            print("Invalid date. Enter 8 digits as YYYYMMDD.")