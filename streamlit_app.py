import streamlit as st
import random
import fractions
import json
import os

# -------------------- Grundeinstellungen --------------------
st.set_page_config(page_title="Lern-App", layout="centered")
st.title("📚 Lern-App")

USERS_FILE = "users.json"
PROGRESS_FILE = "progress.json"

# -------------------- JSON Funktionen --------------------
def load_json(file):
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump({}, f)
    with open(file, "r") as f:
        return json.load(f)

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

users = load_json(USERS_FILE)
progress = load_json(PROGRESS_FILE)

# -------------------- Session State --------------------
if "user" not in st.session_state:
    st.session_state.user = None
if "aufgaben" not in st.session_state:
    st.session_state.aufgaben = []
if "index" not in st.session_state:
    st.session_state.index = 0
if "fertig" not in st.session_state:
    st.session_state.fertig = False
if "checked" not in st.session_state:
    st.session_state.checked = False
if "answer_key" not in st.session_state:
    st.session_state.answer_key = 0

# -------------------- LOGIN --------------------
if st.session_state.user is None:
    st.subheader("🔐 Login / Registrierung")
    username = st.text_input("Benutzername")
    password = st.text_input("Passwort", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Einloggen"):
            if username in users and users[username]["password"] == password:
                st.session_state.user = username
                st.success(f"Willkommen {username} 👋")
                st.rerun()
            else:
                st.error("❌ Falsch")

    with col2:
        if st.button("Registrieren"):
            if username in users:
                st.error("❌ Existiert schon")
            else:
                users[username] = {"password": password}
                save_json(USERS_FILE, users)
                st.success("✅ Account erstellt")

    st.stop()

# -------------------- Aufgaben --------------------
def mathe(klasse, n):
    aufgaben = []
    for _ in range(n):
        a = random.randint(1, 50)
        b = random.randint(1, 50)
        aufgaben.append((f"{a} + {b}", str(a+b)))
    return aufgaben

def deutsch(klasse, n):
    daten = {"Hund":"Hunde","Katze":"Katzen","Haus":"Häuser"}
    return [(f"Plural von {k}", v) for k,v in random.sample(list(daten.items()), n)]

def englisch(klasse, n):
    daten = {"Hund":"dog","Katze":"cat","Haus":"house"}
    return [(f"{k} auf Englisch", v) for k,v in random.sample(list(daten.items()), n)]

# -------------------- Sidebar --------------------
st.sidebar.write(f"👤 {st.session_state.user}")

fach = st.sidebar.selectbox("Fach", ["Mathe", "Deutsch", "Englisch"])
klasse = st.sidebar.slider("Klasse", 1, 10, 5)
anzahl = st.sidebar.slider("Aufgaben", 1, 10, 5)

if st.sidebar.button("Start"):
    if fach == "Mathe":
        st.session_state.aufgaben = mathe(klasse, anzahl)
    elif fach == "Deutsch":
        st.session_state.aufgaben = deutsch(klasse, anzahl)
    else:
        st.session_state.aufgaben = englisch(klasse, anzahl)

    st.session_state.index = 0
    st.session_state.fertig = False
    st.session_state.checked = False
    st.session_state.answer_key += 1
    st.rerun()

# -------------------- QUIZ --------------------
if st.session_state.aufgaben and not st.session_state.fertig:

    frage, loesung = st.session_state.aufgaben[st.session_state.index]

    st.subheader(f"Aufgabe {st.session_state.index+1}")
    st.write(frage)

    antwort = st.text_input(
        "Antwort:",
        key=f"antwort_{st.session_state.answer_key}"
    )

    col1, col2 = st.columns(2)

    # PRÜFEN
    with col1:
        if st.button("Prüfen"):
            st.session_state.checked = True

            if antwort.strip().lower() == loesung.lower():
                st.success("✅ Richtig")
            else:
                st.error(f"❌ Falsch → {loesung}")

            # Fortschritt speichern
            if st.session_state.user not in progress:
                progress[st.session_state.user] = []

            progress[st.session_state.user].append({
                "fach": fach,
                "frage": frage,
                "antwort": antwort,
                "loesung": loesung
            })

            save_json(PROGRESS_FILE, progress)

    # WEITER
    with col2:
        if st.session_state.checked:
            if st.button("Weiter ➡️"):
                st.session_state.index += 1
                st.session_state.checked = False
                st.session_state.answer_key += 1

                if st.session_state.index >= len(st.session_state.aufgaben):
                    st.session_state.fertig = True

                st.rerun()

# -------------------- FERTIG --------------------
elif st.session_state.fertig:
    st.success("🎉 Fertig!")

    if st.button("Nochmal"):
        st.session_state.aufgaben = []
        st.session_state.index = 0
        st.session_state.fertig = False
        st.session_state.checked = False
        st.session_state.answer_key += 1
        st.rerun()

# -------------------- Fortschritt --------------------
st.sidebar.subheader("📊 Fortschritt")

if st.sidebar.button("Anzeigen"):
    if st.session_state.user in progress:
        for e in progress[st.session_state.user]:
            st.write(f"{e['fach']} | {e['frage']} → {e['antwort']} (✔ {e['loesung']})")
    else:
        st.sidebar.info("Noch nichts gemacht")
