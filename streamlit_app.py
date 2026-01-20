import streamlit as st
import random
import json
import os

# ------------------ Dateien ------------------
USERS_FILE = "users.json"
PROGRESS_FILE = "progress.json"

# ------------------ Hilfsfunktionen ------------------
def load_json(file, default):
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump(default, f)
    with open(file, "r") as f:
        return json.load(f)

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

users = load_json(USERS_FILE, {})
progress = load_json(PROGRESS_FILE, {})

# ------------------ Streamlit Setup ------------------
st.set_page_config(page_title="Lern-App", layout="centered")
st.title("🎒 Lern-App")

# ------------------ Session State ------------------
if "user" not in st.session_state:
    st.session_state.user = None
if "task" not in st.session_state:
    st.session_state.task = None
if "solution" not in st.session_state:
    st.session_state.solution = None
if "explanation" not in st.session_state:
    st.session_state.explanation = None
if "feedback" not in st.session_state:
    st.session_state.feedback = None

# ------------------ LOGIN ------------------
if st.session_state.user is None:
    st.subheader("🔐 Login / Registrierung")

    username = st.text_input("Benutzername")
    password = st.text_input("Passwort", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Einloggen"):
            if username in users and users[username] == password:
                st.session_state.user = username
                st.success("Erfolgreich eingeloggt")
                st.rerun()
            else:
                st.error("Falsche Daten")

    with col2:
        if st.button("Registrieren"):
            if username in users:
                st.error("Benutzer existiert schon")
            else:
                users[username] = password
                save_json(USERS_FILE, users)
                progress[username] = []
                save_json(PROGRESS_FILE, progress)
                st.success("Account erstellt")

    st.stop()

# ------------------ Sidebar ------------------
st.sidebar.success(f"👤 {st.session_state.user}")

fach = st.sidebar.radio("Fach wählen", ["Mathe", "Deutsch", "Englisch"])

# ------------------ Aufgaben Generator ------------------
def neue_aufgabe(fach):
    if fach == "Mathe":
        a, b = random.randint(1, 20), random.randint(1, 20)
        return f"{a} + {b}", str(a + b), f"{a} + {b} = {a+b}"

    if fach == "Deutsch":
        daten = {"Hund": "Hunde", "Katze": "Katzen"}
        w, l = random.choice(list(daten.items()))
        return f"Plural von {w}", l, f"Plural von {w} ist {l}"

    if fach == "Englisch":
        daten = {"Hund": "dog", "Katze": "cat"}
        w, l = random.choice(list(daten.items()))
        return f"Übersetze: {w}", l, f"{w} = {l}"

# ------------------ Neue Aufgabe ------------------
if st.sidebar.button("🎲 Neue Aufgabe"):
    task, solution, explanation = neue_aufgabe(fach)
    st.session_state.task = task
    st.session_state.solution = solution
    st.session_state.explanation = explanation
    st.session_state.feedback = None

# ------------------ Aufgabe anzeigen ------------------
if st.session_state.task:
    st.subheader("📝 Aufgabe")
    st.write(st.session_state.task)

    with st.form("answer_form", clear_on_submit=True):
        answer = st.text_input("Deine Antwort")
        submitted = st.form_submit_button("Antwort abgeben")

        if submitted:
            richtig = answer.strip().lower() == st.session_state.solution.lower()

            if richtig:
                st.session_state.feedback = "✅ Richtig!"
            else:
                st.session_state.feedback = f"❌ Falsch! {st.session_state.explanation}"

            progress[st.session_state.user].append({
                "Fach": fach,
                "Aufgabe": st.session_state.task,
                "Richtig": richtig
            })
            save_json(PROGRESS_FILE, progress)

            st.session_state.task = None

# ------------------ Feedback ------------------
if st.session_state.feedback:
    st.info(st.session_state.feedback)

# ------------------ Verlauf ------------------
with st.sidebar.expander("📊 Erledigt"):
    daten = progress.get(st.session_state.user, [])
    if not daten:
        st.write("Noch nichts gemacht")
    else:
        for d in daten:
            emoji = "✅" if d["Richtig"] else "❌"
            st.write(f"{emoji} {d['Fach']} – {d['Aufgabe']}")
