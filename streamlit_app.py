import streamlit as st
import random
import json
import os

# ------------------ DATEIEN ------------------
USERS_FILE = "users.json"

# ------------------ USER LADEN / SPEICHERN ------------------
def load_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

users = load_users()

# ------------------ PAGE ------------------
st.set_page_config(page_title="Lern-App", layout="centered")
st.title("📚 Lern-App")

# ------------------ SESSION STATE ------------------
if "user" not in st.session_state:
    st.session_state.user = None
if "aufgaben" not in st.session_state:
    st.session_state.aufgaben = []
if "index" not in st.session_state:
    st.session_state.index = 0
if "punkte" not in st.session_state:
    st.session_state.punkte = 0
if "quiz_aktiv" not in st.session_state:
    st.session_state.quiz_aktiv = False
if "feedback" not in st.session_state:
    st.session_state.feedback = ""

# ------------------ LOGIN ------------------
if st.session_state.user is None:
    st.subheader("🔐 Login / Registrierung")

    username = st.text_input("Benutzername")
    password = st.text_input("Passwort", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Einloggen"):
            if username in users and users[username]["password"] == password:
                st.session_state.user = username
                st.success("✅ Eingeloggt")
            else:
                st.error("❌ Falsche Daten")

    with col2:
        if st.button("Registrieren"):
            if username in users:
                st.error("❌ Benutzer existiert schon")
            else:
                users[username] = {"password": password}
                save_users(users)
                st.success("✅ Account erstellt")

    st.stop()

# ------------------ AUFGABEN ------------------
def mathe_aufgaben(anzahl, modus, thema):
    tasks = []
    for _ in range(anzahl):
        if modus == "Zufall":
            thema = random.choice(["Plus", "Mal"])

        if thema == "Plus":
            a, b = random.randint(1, 50), random.randint(1, 50)
            tasks.append((f"{a} + {b}", a + b, f"{a} + {b} = {a+b}"))
        elif thema == "Mal":
            a, b = random.randint(2, 10), random.randint(2, 10)
            tasks.append((f"{a} × {b}", a * b, f"{a} × {b} = {a*b}"))

    return tasks

# ------------------ SIDEBAR ------------------
st.sidebar.write(f"👤 Eingeloggt als: {st.session_state.user}")
st.sidebar.header("⚙️ Einstellungen")

klasse = st.sidebar.slider("Klassenstufe", 1, 10, 4)
modus = st.sidebar.radio("Modus", ["Zufall", "Thema"])

thema = "Plus"
if modus == "Thema":
    thema = st.sidebar.selectbox("Thema", ["Plus", "Mal"])

anzahl = st.sidebar.slider("Anzahl Aufgaben", 1, 10, 5)

if st.sidebar.button("▶️ Quiz starten"):
    st.session_state.aufgaben = mathe_aufgaben(anzahl, modus, thema)
    st.session_state.index = 0
    st.session_state.punkte = 0
    st.session_state.quiz_aktiv = True
    st.session_state.feedback = ""

if st.sidebar.button("⛔ Abbrechen"):
    st.session_state.quiz_aktiv = False
    st.session_state.aufgaben = []

# ------------------ QUIZ ------------------
if st.session_state.quiz_aktiv:
    if st.session_state.index < len(st.session_state.aufgaben):
        frage, lösung, erklärung = st.session_state.aufgaben[st.session_state.index]

        st.subheader(f"Aufgabe {st.session_state.index + 1}")
        st.write(frage)

        antwort = st.text_input("Antwort", key=f"antwort_{st.session_state.index}")

        if st.button("✔️ Abgeben"):
            if antwort.strip() == str(lösung):
                st.session_state.punkte += 1
                st.session_state.feedback = "✅ Richtig!"
            else:
                st.session_state.feedback = f"❌ Falsch! {erklärung}"

            st.session_state.index += 1

        if st.session_state.feedback:
            st.info(st.session_state.feedback)

    else:
        st.success("🎉 Quiz beendet")
        st.write(f"Punkte: {st.session_state.punkte} / {len(st.session_state.aufgaben)}")
        st.session_state.quiz_aktiv = False
