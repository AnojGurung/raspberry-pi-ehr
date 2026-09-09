import sqlite3

import pandas as pd

conn = sqlite3.connect("ehr.db")

df = pd.read_sql_query(
    "SELECT * FROM vitals WHERE patient_id = 2;", conn)

conn.close()
print(df)