import streamlit as st
import sqlite3
import pandas as pd
import os

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Smart Hospital System", layout="wide")

if not os.path.exists("uploads"):
    os.makedirs("uploads")

# ---------------- DATABASE ----------------
def get_conn():
    return sqlite3.connect("hospital.db", check_same_thread=False)

def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS patients(
        patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        gender TEXT,
        phone TEXT,
        department TEXT
    )
    """)

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

    conn.commit()
    conn.close()

init_db()

# ---------------- AI CHATBOT ----------------
def ai_chatbot(symptoms):
    s = symptoms.lower()

    if "chest" in s or "heart" in s:
        return "🫀 Go to Cardiology"
    elif "head" in s or "memory" in s:
        return "🧠 Go to Neurology"
    elif "bone" in s or "fracture" in s:
        return "🦴 Go to Orthopedic"
    elif "ear" in s or "throat" in s:
        return "👂 Go to ENT"
    else:
        return "🏥 Go to General Medicine"

# ---------------- LOGIN ----------------
st.title("🏥 Smart Hospital Management System")

if "login" not in st.session_state:
    st.session_state.login = False

menu = st.sidebar.selectbox("Menu", [
    "Login",
    "Dashboard",
    "Register Patient",
    "View Patients",
    "Doctor Consultation",
    "Upload Reports",
    "Patient Portal",
    "AI Chatbot"
])

# ---------------- LOGIN PAGE ----------------
if menu == "Login":

    st.subheader("Admin Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username == "admin" and password == "admin123":
            st.session_state.login = True
            st.success("Login Successful")
        else:
            st.error("Invalid Credentials")

# ---------------- DASHBOARD ----------------
elif menu == "Dashboard":

    conn = get_conn()

    total_patients = pd.read_sql_query("SELECT COUNT(*) as c FROM patients", conn).iloc[0]["c"]
    total_consult = pd.read_sql_query("SELECT COUNT(*) as c FROM consultations", conn).iloc[0]["c"]

    st.subheader("📊 Dashboard")
    st.metric("Total Patients", total_patients)
    st.metric("Total Consultations", total_consult)

    conn.close()

# ---------------- REGISTER PATIENT ----------------
elif menu == "Register Patient":

    st.subheader("Register Patient")

    name = st.text_input("Name")
    age = st.number_input("Age", 1, 120)
    gender = st.selectbox("Gender", ["Male", "Female"])
    phone = st.text_input("Phone")

    department = st.selectbox("Department", [
        "Cardiology", "Neurology", "Orthopedic", "ENT", "General Medicine"
    ])

    if st.button("Register"):

        conn = get_conn()
        c = conn.cursor()

        c.execute("""
        INSERT INTO patients(name, age, gender, phone, department)
        VALUES (?, ?, ?, ?, ?)
        """, (name, age, gender, phone, department))

        conn.commit()
        conn.close()

        st.success("Patient Registered Successfully")

# ---------------- VIEW PATIENTS ----------------
elif menu == "View Patients":

    st.subheader("Patient Records")

    conn = get_conn()
    df = pd.read_sql_query("SELECT * FROM patients", conn)
    conn.close()

    st.dataframe(df)

# ---------------- CONSULTATION ----------------
elif menu == "Doctor Consultation":

    st.subheader("Doctor Consultation")

    pid = st.number_input("Patient ID", min_value=1)
    symptoms = st.text_area("Symptoms")
    diagnosis = st.text_input("Diagnosis")
    medicines = st.text_area("Medicines")
    notes = st.text_area("Notes")

    if st.button("Save"):

        conn = get_conn()
        c = conn.cursor()

        c.execute("""
        INSERT INTO consultations(patient_id, symptoms, diagnosis, medicines, notes)
        VALUES (?, ?, ?, ?, ?)
        """, (pid, symptoms, diagnosis, medicines, notes))

        conn.commit()
        conn.close()

        st.success("Saved Successfully")

# ---------------- UPLOAD REPORTS ----------------
elif menu == "Upload Reports":

    st.subheader("Upload Reports")

    pid = st.number_input("Patient ID", min_value=1)
    file = st.file_uploader("Upload File", type=["pdf", "png", "jpg"])

    if file:
        path = os.path.join("uploads", file.name)

        with open(path, "wb") as f:
            f.write(file.getbuffer())

        st.success("Report Uploaded")

# ---------------- PATIENT PORTAL ----------------
elif menu == "Patient Portal":

    st.subheader("Patient Portal")

    pid = st.number_input("Enter Patient ID", min_value=1)

    if st.button("Search"):

        conn = get_conn()

        patient = pd.read_sql_query(f"SELECT * FROM patients WHERE patient_id={pid}", conn)
        history = pd.read_sql_query(f"SELECT * FROM consultations WHERE patient_id={pid}", conn)

        st.write("### Patient Info")
        st.dataframe(patient)

        st.write("### Medical History")
        st.dataframe(history)

# ---------------- AI CHATBOT ----------------
elif menu == "AI Chatbot":

    st.subheader("🤖 AI Health Chatbot")

    symptoms = st.text_input("Enter Symptoms")

    if st.button("Check"):

        if symptoms:
            result = ai_chatbot(symptoms)
            st.success(result)
        else:
            st.warning("Enter symptoms first")
