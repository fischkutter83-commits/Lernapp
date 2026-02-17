import streamlit as st
import random
import json
import os

st.set_page_config(page_title="Lern-App")
st.title("📚 Lern-App")

USERS_FILE = "users.json"
PROGRESS_FILE = "progress.json"

# ---------------- JSON safe laden ----------------
def load_json(file):
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump({}, f)
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return {}

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f)

users = load_json(USERS_FILE)
progress = load_json(PROGRESS_FILE)

# ---------------- Session ----------------
if "user" not in st.session_state:
    st.session_state.user = None
if "aufgaben" not in st.session_state:
    st.session_state.aufgaben = []
if "index" not in st.session_state:
    st.session_state.index = 0
if "checked" not in st.session_state:
    st.session_state.checked = False
if "antwort" not in st.session_state:
    st.session_state.antwort = ""

# ---------------- LOGIN ----------------
if st.session_state.user is None:
    st.subheader("Login")

    username = st.text_input("Name")
    password = st.text_input("Passwort", type="password")

    if st.button("Einloggen"):
        if username in users and users[username] == password:
            st.session_state.user = username
            st.rerun()
        else:
            st.error("Falsch")

    if st.button("Registrieren"):
        users[username] = password
        save_json(USERS_FILE, users)
        st.success("Account erstellt")

    st.stop()

# ---------------- Aufgaben ----------------
def mathe():
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    return f"{a}+{b}", str(a+b)

def deutsch():
    return "Plural von Hund", "Hunde"

def englisch():
    return "Hund auf Englisch", "dog"

# ---------------- Sidebar ----------------
st.sidebar.write(f"👤 {st.session_state.user}")

fach = st.sidebar.selectbox("Fach", ["Mathe", "Deutsch", "Englisch"])

if st.sidebar.button("Start"):
    st.session_state.index = 0
    st.session_state.checked = False
    st.session_state.aufgaben = []

    for _ in range(5):
        if fach == "Mathe":
            st.session_state.aufgaben.append(mathe())
        elif fach == "Deutsch":
            st.session_state.aufgaben.append(deutsch())
        else:
            st.session_state.aufgaben.append(englisch())

# ---------------- Quiz ----------------
if st.session_state.aufgaben:
    frage, lösung = st.session_state.aufgaben[st.session_state.index]

    st.write(f"Aufgabe {st.session_state.index+1}")
    st.write(frage)

    antwort = st.text_input("Antwort", key="input")

    if not st.session_state.checked:
        if st.button("Prüfen"):
            if antwort == lösung:
                st.success("Richtig")
            else:
                st.error(f"Falsch! Lösung: {lösung}")

            st.session_state.checked = True

            # speichern
            if st.session_state.user not in progress:
                progress[st.session_state.user] = []

            progress[st.session_state.user].append({
                "frage": frage,
                "antwort": antwort,
                "lösung": lösung
            })

            save_json(PROGRESS_FILE, progress)

    else:
        if st.button("Weiter"):
            st.session_state.index += 1
            st.session_state.checked = False
            st.session_state.antwort = ""
            st.rerun()

            if st.session_state.index >= len(st.session_state.aufgaben):
                st.success("Fertig!")
