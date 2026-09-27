import pandas as pd

vitals = pd.read_csv("vitals.csv")
sessions = pd.read_csv("pulse_sessions.csv")
beats = pd.read_csv("pulse_beats.csv")


print("\n---VITALS---")
print(vitals.head())

print("\n---PULSE SESSIONS---")
print(sessions.head())

print("\n---BEATS---")
print(beats.head())


