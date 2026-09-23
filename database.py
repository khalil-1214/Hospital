import sqlite3
from contextlib import contextmanager

DB_NAME = "hospital.db"

@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init_db():
    with get_conn() as conn:
        c = conn.cursor()

        c.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialty TEXT,
            education TEXT,
            experience INTEGER,
            fee INTEGER,
            available TEXT
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            phone TEXT,
            password TEXT
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient TEXT NOT NULL,
            doctor_id INTEGER,
            date TEXT,
            time TEXT,
            status TEXT DEFAULT 'زیرِ التوا'
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient TEXT,
            doctor_id INTEGER,
            date TEXT,
            diagnosis TEXT,
            prescription TEXT
        )
        """)

def db_empty():
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM doctors")
        return c.fetchone()[0] == 0

# ---------- Doctors ----------
def add_doctor(name, specialty, education, experience, fee, available):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO doctors (name, specialty, education, experience, fee, available) VALUES (?,?,?,?,?,?)",
            (name, specialty, education, experience, fee, available)
        )

def get_doctors():
    with get_conn() as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM doctors").fetchall()]

def delete_doctor(doctor_id):
    with get_conn() as conn:
        conn.execute("DELETE FROM doctors WHERE id=?", (doctor_id,))

# ---------- Patients ----------
def add_patient(name, age, gender, phone, password=""):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO patients (name, age, gender, phone, password) VALUES (?,?,?,?,?)",
            (name, age, gender, phone, password)
        )

def get_patients():
    with get_conn() as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM patients").fetchall()]

def delete_patient(patient_id):
    with get_conn() as conn:
        conn.execute("DELETE FROM patients WHERE id=?", (patient_id,))

# ---------- Appointments ----------
def add_appointment(patient, doctor_id, date, time, status="زیرِ التوا"):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO appointments (patient, doctor_id, date, time, status) VALUES (?,?,?,?,?)",
            (patient, doctor_id, date, time, status)
        )

def get_appointments():
    with get_conn() as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM appointments").fetchall()]

def get_patient_appointments(patient):
    with get_conn() as conn:
        return [dict(r) for r in conn.execute(
            "SELECT * FROM appointments WHERE patient=?", (patient,)
        ).fetchall()]

def update_appointment_status(appt_id, status):
    with get_conn() as conn:
        conn.execute("UPDATE appointments SET status=? WHERE id=?", (status, appt_id))

def delete_appointment(appt_id):
    with get_conn() as conn:
        conn.execute("DELETE FROM appointments WHERE id=?", (appt_id,))

# ---------- Reports ----------
def add_report(patient, doctor_id, date, diagnosis, prescription):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO reports (patient, doctor_id, date, diagnosis, prescription) VALUES (?,?,?,?,?)",
            (patient, doctor_id, date, diagnosis, prescription)
        )

def get_reports():
    with get_conn() as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM reports").fetchall()]

def get_patient_reports(patient):
    with get_conn() as conn:
        return [dict(r) for r in conn.execute(
            "SELECT * FROM reports WHERE patient=?", (patient,)
        ).fetchall()]
