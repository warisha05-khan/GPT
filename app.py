import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# --------------------------
# DATABASE
# --------------------------
conn = sqlite3.connect("hospital.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS patients(
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    phone TEXT,
    address TEXT,
    disease TEXT,
    registration_date TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS appointments(
    appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_name TEXT,
    doctor_name TEXT,
    appointment_date TEXT,
    appointment_time TEXT,
    status TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS history(
    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_name TEXT,
    visit_date TEXT,
    diagnosis TEXT,
    treatment TEXT,
    notes TEXT
)
""")

conn.commit()

# --------------------------
# PAGE CONFIG
# --------------------------
st.set_page_config(
    page_title="ICT Health Management System",
    page_icon="🏥",
    layout="wide"
)

# --------------------------
# CUSTOM CSS
# --------------------------
st.markdown("""
<style>
.main {
    background-color: #f8fbff;
}

.title {
    text-align:center;
    color:#0f62fe;
    font-size:40px;
    font-weight:bold;
}

.subtitle {
    text-align:center;
    color:gray;
    font-size:18px;
}

.roll {
    background:#0f62fe;
    color:white;
    padding:10px;
    border-radius:10px;
    text-align:center;
    font-weight:bold;
}

.card {
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0px 0px 10px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# --------------------------
# HEADER
# --------------------------
st.markdown("<div class='title'>🏥 ICT in Health Management System</div>", unsafe_allow_html=True)

st.markdown("""
<div class='subtitle'>
Smart Hospital Management using ICT
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='roll'>
Group Members Roll Numbers:
14 | 42 | 43 | 46 | 118
</div>
""", unsafe_allow_html=True)

st.write("")

# --------------------------
# SIDEBAR
# --------------------------
menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Patient Registration",
        "Doctor Appointment",
        "Patient History",
        "View Records",
        "ICT in Health Ideas"
    ]
)

# --------------------------
# DASHBOARD
# --------------------------
if menu == "Dashboard":

    st.header("Hospital Dashboard")

    col1, col2, col3 = st.columns(3)

    patient_count = c.execute(
        "SELECT COUNT(*) FROM patients"
    ).fetchone()[0]

    appointment_count = c.execute(
        "SELECT COUNT(*) FROM appointments"
    ).fetchone()[0]

    history_count = c.execute(
        "SELECT COUNT(*) FROM history"
    ).fetchone()[0]

    col1.metric("Registered Patients", patient_count)
    col2.metric("Appointments", appointment_count)
    col3.metric("Medical Histories", history_count)

    st.image(
        "https://images.unsplash.com/photo-1576091160550-2173dba999ef",
        use_container_width=True
    )

# --------------------------
# PATIENT REGISTRATION
# --------------------------
elif menu == "Patient Registration":

    st.header("🧑 Patient Registration")

    with st.form("register_form"):

        name = st.text_input("Patient Name")
        age = st.number_input("Age", 1, 120)
        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other"]
        )
        phone = st.text_input("Phone Number")
        address = st.text_area("Address")
        disease = st.text_input("Disease / Problem")

        submit = st.form_submit_button("Register Patient")

        if submit:

            c.execute("""
            INSERT INTO patients
            (name, age, gender, phone, address, disease, registration_date)
            VALUES (?,?,?,?,?,?,?)
            """,
            (
                name,
                age,
                gender,
                phone,
                address,
                disease,
                str(datetime.now())
            ))

            conn.commit()

            st.success("Patient Registered Successfully")

# --------------------------
# APPOINTMENT
# --------------------------
elif menu == "Doctor Appointment":

    st.header("📅 Online Doctor Appointment")

    with st.form("appointment_form"):

        patient_name = st.text_input("Patient Name")

        doctor_name = st.selectbox(
            "Select Doctor",
            [
                "Dr. Ahmed",
                "Dr. Ali",
                "Dr. Fatima",
                "Dr. Hassan"
            ]
        )

        appointment_date = st.date_input(
            "Appointment Date"
        )

        appointment_time = st.time_input(
            "Appointment Time"
        )

        submit = st.form_submit_button(
            "Book Appointment"
        )

        if submit:

            c.execute("""
            INSERT INTO appointments
            (patient_name, doctor_name,
            appointment_date,
            appointment_time, status)
            VALUES (?,?,?,?,?)
            """,
            (
                patient_name,
                doctor_name,
                str(appointment_date),
                str(appointment_time),
                "Pending"
            ))

            conn.commit()

            st.success(
                "Appointment Booked Successfully"
            )

# --------------------------
# PATIENT HISTORY
# --------------------------
elif menu == "Patient History":

    st.header("📖 Patient Medical History")

    with st.form("history_form"):

        patient_name = st.text_input("Patient Name")

        visit_date = st.date_input(
            "Visit Date"
        )

        diagnosis = st.text_area(
            "Diagnosis"
        )

        treatment = st.text_area(
            "Treatment"
        )

        notes = st.text_area(
            "Doctor Notes"
        )

        submit = st.form_submit_button(
            "Save History"
        )

        if submit:

            c.execute("""
            INSERT INTO history
            (patient_name, visit_date,
            diagnosis, treatment, notes)
            VALUES (?,?,?,?,?)
            """,
            (
                patient_name,
                str(visit_date),
                diagnosis,
                treatment,
                notes
            ))

            conn.commit()

            st.success(
                "Patient History Saved"
            )

# --------------------------
# VIEW RECORDS
# --------------------------
elif menu == "View Records":

    st.header("📊 Hospital Records")

    option = st.selectbox(
        "Choose Data",
        [
            "Patients",
            "Appointments",
            "History"
        ]
    )

    if option == "Patients":

        df = pd.read_sql_query(
            "SELECT * FROM patients",
            conn
        )

        st.dataframe(
            df,
            use_container_width=True
        )

    elif option == "Appointments":

        df = pd.read_sql_query(
            "SELECT * FROM appointments",
            conn
        )

        st.dataframe(
            df,
            use_container_width=True
        )

    elif option == "History":

        df = pd.read_sql_query(
            "SELECT * FROM history",
            conn
        )

        st.dataframe(
            df,
            use_container_width=True
        )

# --------------------------
# ICT IN HEALTH
# --------------------------
elif menu == "ICT in Health Ideas":

    st.header("💡 ICT Applications in Healthcare")

    ideas = [
        "Electronic Health Records (EHR)",
        "Telemedicine & Online Consultation",
        "AI Disease Prediction",
        "Online Appointment Systems",
        "Remote Patient Monitoring",
        "Smart Hospital Management",
        "Medical IoT Devices",
        "Health Mobile Applications",
        "Cloud Based Medical Records",
        "Digital Prescription System",
        "Health Chatbots",
        "Medical Imaging Analysis using AI",
        "Emergency Ambulance Tracking",
        "Wearable Health Monitoring",
        "Big Data Analytics in Healthcare"
    ]

    for idea in ideas:
        st.success(idea)

    st.subheader("Future Enhancements")

    st.write("""
    - Doctor Login
    - Admin Dashboard
    - Patient Login
    - SMS Appointment Reminder
    - Email Notification
    - AI Symptom Checker
    - Online Payments
    - Prescription Generator
    - Lab Report Upload
    - Cloud Database Integration
    """)
