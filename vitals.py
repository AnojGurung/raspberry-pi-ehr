import sqlite3
from datetime import datetime

from validation import get_valid_date

from pulse_sensor import get_heart_rate


DATABASE = "ehr.db"


def add_vitals():
    patient_id = input("Enter patient id: ")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM patients WHERE patient_id = ?",
        (patient_id,)
    )

    patient = cursor.fetchone()

    if not patient:
        print("Patient not found.")
        conn.close()
        return

    measurement_date = get_valid_date(
        "Measurement date (YYYYMMDD): "
    )

    result = get_heart_rate()

    if result is None:
        print("Heart rate measurement failed.")
        conn.close()
        return

    # Get values returned from pulse_sensor.py
    bpm = result["bpm"]
    beat_times = result["beat_times"]
    intervals = result["intervals"]
    median_interval = result["median_interval"]

    # --------------------------------
    # SAVE FINAL BPM TO VITALS
    # --------------------------------

    cursor.execute("""
        INSERT INTO vitals (
            patient_id,
            measurement_date,
            heart_rate
        )
        VALUES (?, ?, ?)
    """, (
        patient_id,
        measurement_date,
        bpm
    ))

    # --------------------------------
    # SAVE PULSE SESSION
    # --------------------------------

    measurement_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
        INSERT INTO pulse_sessions (
            patient_id,
            measurement_time,
            final_bpm,
            beats_detected,
            median_interval
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        patient_id,
        measurement_time,
        bpm,
        len(beat_times),
        median_interval
    ))

    session_id = cursor.lastrowid

    # --------------------------------
    # SAVE EVERY DETECTED BEAT
    # --------------------------------

    for i, beat_time in enumerate(beat_times):

        if i == 0:
            interval = None
            beat_bpm = None

        else:
            interval = intervals[i - 1]
            beat_bpm = 60 / interval

        cursor.execute("""
            INSERT INTO pulse_beats (
                session_id,
                beat_number,
                beat_time,
                interval_seconds,
                beat_bpm
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            session_id,
            i + 1,
            beat_time,
            interval,
            beat_bpm
        ))

    conn.commit()
    conn.close()

    print("\nVitals added successfully.")
    print("Heart rate:", bpm, "BPM")
    print("Beats detected:", len(beat_times))
    print("Pulse session ID:", session_id)


def show_patient_vitals():
    patient_id = input("Enter patient id: ")
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute("""
                    SELECT vital_id,
                    measurement_date,
                    heart_rate
                    FROM vitals WHERE patient_id =?
                    ORDER BY measurement_date
                    """, (patient_id,))
    
    vitals = cursor.fetchall()
    conn.close()
    
    if not vitals:
        print("No vitals found for this patient.")
        return
    
    print("\n---PATIENT VITALS---")
    
    for vital in vitals:
        print(f"Vital ID: {vital[0]} | "
              f"Data: {vital[1]} | "
              f"Heart rate: {vital[2]} BPM"
              )
        
if __name__=="__main__":
    add_vitals()
    
    
    