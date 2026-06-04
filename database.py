import sqlite3

conn = sqlite3.connect("hospital.db")
c = conn.cursor()

# Patients Table
c.execute("""
CREATE TABLE IF NOT EXISTS patients(
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    phone TEXT,
    address TEXT,
    blood_group TEXT
)
""")

# Consultations Table
c.execute("""
CREATE TABLE IF NOT EXISTS consultations(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    symptoms TEXT,
    diagnosis TEXT,
    medicines TEXT,
    notes TEXT
)
""")

# Doctors Table (optional)
c.execute("""
CREATE TABLE IF NOT EXISTS doctors(
    doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    password TEXT
)
""")

conn.commit()
conn.close()

print("Database created successfully!")
