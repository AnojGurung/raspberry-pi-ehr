import sqlite3

import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

conn = sqlite3.connect("ehr.db")

df = pd.read_sql_query(
    """
    SELECT patient_id, measurement_date, heart_rate
    FROM vitals
    WHERE patient_id = 2
    ORDER BY measurement_date
    """, conn)

conn.close()

df["measurement_date"] = pd.to_datetime(df["measurement_date"])

print("\n---HEART RATE DATA---")
print(df)


print("Mean heart rate: ", df["heart_rate"].mean())
print("Median heart rate: ", df["heart_rate"].median())
print("Standard deviation : ", df["heart_rate"].std())
print("Minimum heart rate: ", df["heart_rate"].min())
print("Maximum heart rate: ", df["heart_rate"].max())

df["heart_rate_change"] = df["heart_rate"].diff()


print(df[["measurement_date",
          "heart_rate",
          "heart_rate_change"
            ]])

# plt.plot(
#         df["measurement_date"],
#         df["heart_rate"],
#         marker = "o"
#     )
# plt.xlabel("Measurement_date")
# plt.ylabel("Heart Rate (BPM)")
# plt.title("Heart Rate Over Time")
# 
# plt.xticks(rotation=45)
# plt.tight_layout()
# 
# plt.show()
# 

# regression
#df["heart_rate_change"] = df["heart_rate"].diff()
df["days_from_start"] = (df["measurement_date"] - df["measurement_date"].min()
                         ).dt.days
model = smf.ols("heart_rate ~ days_from_start",
                data=df
                ).fit()
print(model.summary())


