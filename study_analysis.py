import sqlite3
import pandas as pd
import statsmodels.formula.api as smf

DATABASE = "ehr.db"

conn = sqlite3.connect(DATABASE)

df = pd.read_sql_query("""
    SELECT *
    FROM study_data
""", conn)

conn.close()

df["measurement_date"] = pd.to_datetime(df["measurement_date"])

print("\n--- STUDY DATA ---")
print(df.head())

print("\nNumber of rows:", len(df))
print("Number of patients:", df["patient_id"].nunique())


# -------------------------
# LINEAR REGRESSION
# -------------------------

model = smf.ols(
    "systolic_bp ~ age + bmi + smoking + treatment",
    data=df
).fit()

print("\n--- LINEAR REGRESSION ---")
print(model.summary())

# -------------------------
# MIXED-EFFECTS MODEL
# -------------------------

mixed_model = smf.mixedlm(
    "systolic_bp ~ age + bmi + smoking + treatment",
    data=df,
    groups=df["patient_id"]
).fit()

print("\n--- MIXED-EFFECTS MODEL ---")
print(mixed_model.summary())