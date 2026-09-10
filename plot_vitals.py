import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("ehr.db")

df = pd.read_sql_query("""
    SELECT measurement_date,
           heart_rate
    FROM vitals
    WHERE patient_id = 2
    ORDER BY measurement_date
""", conn)

conn.close()

df["measurement_date"] = pd.to_datetime(df["measurement_date"])

plt.plot(
    df["measurement_date"],
    df["heart_rate"],
    marker="o"
)

plt.xlabel("Measurement Date")
plt.ylabel("Heart Rate (BPM)")
plt.title("Heart Rate Over Time")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()