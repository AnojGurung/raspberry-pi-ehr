import sqlite3
import random
from datetime import datetime, timedelta

DATABASE = "ehr.db"

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

# Get existing patient IDs
cursor.execute("SELECT patient_id, sex, dob FROM patients")
patients = cursor.fetchall()

if not patients:
    print("No patients found. Add patients first.")
    conn.close()
    raise SystemExit

for patient_id, sex, dob in patients:

    birth_date = datetime.strptime(dob, "%Y-%m-%d")
    age = 2026 - birth_date.year

    practice_id = random.choice([1, 2, 3])
    deprivation_score = round(random.uniform(1, 10), 1)
    smoking = random.choice([0, 1])
    treatment = random.choice([0, 1])

    start_date = datetime(2026, 1, 10)

    base_bmi = random.uniform(22, 34)
    base_bp = random.randint(120, 155)
    base_hr = random.randint(65, 90)

    hospitalized = random.choice([0, 0, 0, 1])

    hospitalization_date = None

    if hospitalized == 1:
        hospitalization_date = (
            start_date + timedelta(days=random.randint(60, 220))
        ).strftime("%Y-%m-%d")

    for measurement_number in range(5):

        measurement_date = (
            start_date + timedelta(days=measurement_number * 60)
        )

        bmi = base_bmi + random.uniform(-1.5, 1.5)

        systolic_bp = (
            base_bp
            - treatment * measurement_number * random.uniform(1, 3)
            + random.uniform(-5, 5)
        )

        heart_rate = (
            base_hr
            - treatment * measurement_number * random.uniform(0.5, 2)
            + random.uniform(-4, 4)
        )

        cursor.execute("""
            INSERT INTO study_data (
                patient_id,
                age,
                sex,
                practice_id,
                deprivation_score,
                smoking,
                measurement_date,
                bmi,
                systolic_bp,
                heart_rate,
                treatment,
                hospitalized,
                hospitalization_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            patient_id,
            age,
            sex,
            practice_id,
            deprivation_score,
            smoking,
            measurement_date.strftime("%Y-%m-%d"),
            round(bmi, 1),
            round(systolic_bp),
            round(heart_rate),
            treatment,
            hospitalized,
            hospitalization_date
        ))

conn.commit()
conn.close()

print("Synthetic longitudinal study data added successfully.")

# print(df.shape)
# print(df.columns)
# print(df[["systolic_bp", "age", "bmi", "smoking", "treatment"]].head(10))
# print(df[["systolic_bp", "age", "bmi", "smoking", "treatment"]].isna().sum())
# print(df["smoking"].value_counts())
# print(df["treatment"].value_counts())

