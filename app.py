import streamlit as st
import sqlite3
import pandas as pd
import os

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Hospital Management System")

if not os.path.exists("uploads"):
    os.makedirs("uploads")

# ---------------- DATABASE ----------------
def get_connection():
    return sqlite3.connect("hospital.db", check_same_thread=False)

# ---------------- LOGIN ----------------
st.title("🏥 Hospital Management System")

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Admin Login",
        "Register Patient",
        "View Patients",
        "Doctor Consultation",
        "Upload Reports",
        "Patient Portal"
    ]
)

# ---------------- ADMIN LOGIN ----------------
if menu == "Admin Login":
    st.subheader("Admin Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.success("Login successful")
        else:
            st.error("Invalid credentials")

# ---------------- REGISTER PATIENT ----------------
elif menu == "Register Patient":
    st.subheader("Register Patient")

    name = st.text_input("Name")
    age = st.number_input("Age", 1, 120)
    gender = st.selectbox("Gender", ["Male", "Female"])
    phone = st.text_input("Phone")
    address = st.text_area("Address")
    blood = st.text_input("Blood Group")

    if st.button("Save Patient"):
        conn = get_connection()
        c = conn.cursor()

        c.execute("""
        INSERT INTO patients(name, age, gender, phone, address, blood_group)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (name, age, gender, phone, address, blood))

        conn.commit()
        conn.close()

        st.success("Patient registered successfully!")

# ---------------- VIEW PATIENTS ----------------
elif menu == "View Patients":
    st.subheader("All Patients")

    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM patients", conn)
    conn.close()

    st.dataframe(df)

# ---------------- DOCTOR CONSULTATION ----------------
elif menu == "Doctor Consultation":
    st.subheader("Doctor Consultation")

    patient_id = st.number_input("Patient ID", min_value=1)
    symptoms = st.text_area("Symptoms")
    diagnosis = st.text_input("Diagnosis")
    medicines = st.text_area("Medicines")
    notes = st.text_area("Doctor Notes")

    if st.button("Save Consultation"):
        conn = get_connection()
        c = conn.cursor()

        c.execute("""
        INSERT INTO consultations(patient_id, symptoms, diagnosis, medicines, notes)
        VALUES (?, ?, ?, ?, ?)
        """, (patient_id, symptoms, diagnosis, medicines, notes))

        conn.commit()
        conn.close()

        st.success("Consultation saved!")

# ---------------- UPLOAD REPORTS ----------------
elif menu == "Upload Reports":
    st.subheader("Upload Patient Reports")

    patient_id = st.number_input("Patient ID", min_value=1)
    file = st.file_uploader("Upload Report (PDF/Image)", type=["pdf", "png", "jpg"])

    if file is not None:
        path = os.path.join("uploads", file.name)

        with open(path, "wb") as f:
            f.write(file.getbuffer())

        st.success("Report uploaded successfully!")

# ---------------- PATIENT PORTAL ----------------
elif menu == "Patient Portal":
    st.subheader("Patient Portal")

    pid = st.number_input("Enter Patient ID", min_value=1)

    if st.button("Search"):
        conn = get_connection()

        patient = pd.read_sql_query(
            f"SELECT * FROM patients WHERE patient_id={pid}",
            conn
        )

        history = pd.read_sql_query(
            f"SELECT * FROM consultations WHERE patient_id={pid}",
            conn
        )

        conn.close()

        st.write("### Patient Info")
        st.dataframe(patient)

        st.write("### Medical History")
        st.dataframe(history)
