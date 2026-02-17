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

# -------------------- JSON Laden / Speichern --------------------
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
if "antwort" not in st.session_state:
    st.session_state.antwort = ""
if "checked" not in st.session_state:
    st.session_state.checked = False

# -------------------- LOGIN --------------------
if st.session_state.user is None:
    st.subheader("🔐 Login / Registrierung")

    username = st.text_input("Benutzername")
    password = st.text_input("Passwort", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Einloggen"):
            if username in users:
                user_data = users[username]

                # unterstützt alte und neue Struktur
                if isinstance(user_data, str):
                    saved_password = user_data
                else:
                    saved_password = user_data.get("password", "")

                if saved_password == password:
                    st.session_state.user = username
                    st.success(f"Willkommen {username} 👋")
                    st.rerun()
                else:
                    st.error("❌ Falsches Passwort")
            else:
                st.error("❌ Benutzer existiert nicht")

    with col2:
        if st.button("Registrieren"):
            if username in users:
                st.error("❌ Benutzer existiert bereits")
            else:
                users[username] = {"password": password}
                save_json(USERS_FILE, users)
                st.success("✅ Account erstellt – bitte einloggen")

    st.stop()

# -------------------- Aufgaben --------------------
def generiere_mathe(anzahl):
    aufgaben = []
    for _ in range(anzahl):
        a, b = random.randint(1, 20), random.randint(1, 20)
        aufgaben.append((f"{a} + {b}", str(a+b)))
    return aufgaben

def generiere_deutsch(anzahl):
    wörter = {"Hund":"Hunde","Katze":"Katzen","Auto":"Autos"}
    aufgaben = []
    for _ in range(anzahl):
        wort, lösung = random.choice(list(wörter.items()))
        aufgaben.append((f"Plural von {wort}", lösung))
    return aufgaben

def generiere_englisch(anzahl):
    wörter = {"Hund":"dog","Katze":"cat","Haus":"house"}
    aufgaben = []
    for _ in range(anzahl):
        de, en = random.choice(list(wörter.items()))
        aufgaben.append((f"Übersetze: {de}", en))
    return aufgaben

# -------------------- Sidebar --------------------
st.sidebar.write(f"👤 {st.session_state.user}")

fach = st.sidebar.selectbox("Fach", ["Mathe", "Deutsch", "Englisch"])
anzahl = st.sidebar.slider("Anzahl Aufgaben", 1, 10, 5)

if st.sidebar.button("Start"):
    if fach == "Mathe":
        st.session_state.aufgaben = generiere_mathe(anzahl)
    elif fach == "Deutsch":
        st.session_state.aufgaben = generiere_deutsch(anzahl)
    else:
        st.session_state.aufgaben = generiere_englisch(anzahl)

    st.session_state.index = 0
    st.session_state.fertig = False
    st.session_state.antwort = ""
    st.session_state.checked = False
    st.rerun()

# -------------------- Quiz --------------------
if st.session_state.aufgaben and not st.session_state.fertig:

    frage, lösung = st.session_state.aufgaben[st.session_state.index]

    st.subheader(f"Aufgabe {st.session_state.index + 1}")
    st.write(frage)

    antwort = st.text_input("Deine Antwort", key=f"antwort_{st.session_state.index}")

    col1, col2 = st.columns(2)

    # ---------------- PRÜFEN ----------------
    with col1:
        if st.button("Prüfen") and not st.session_state.checked:
            st.session_state.checked = True

            if antwort.strip().lower() == lösung.lower():
                st.success("✅ Richtig")
            else:
                st.error(f"❌ Falsch – richtige Antwort: {lösung}")

            # speichern
            if st.session_state.user not in progress:
                progress[st.session_state.user] = []

            progress[st.session_state.user].append({
                "frage": frage,
                "deine_antwort": antwort,
                "lösung": lösung
            })

            save_json(PROGRESS_FILE, progress)

    # ---------------- NÄCHSTE ----------------
    with col2:
        if st.button("Weiter"):
            st.session_state.index += 1
            st.session_state.checked = False

            if st.session_state.index >= len(st.session_state.aufgaben):
                st.session_state.fertig = True

            st.rerun()

# -------------------- ENDE --------------------
elif st.session_state.fertig:
    st.success("🎉 Fertig!")

    if st.button("Nochmal"):
        st.session_state.aufgaben = []
        st.session_state.index = 0
        st.session_state.fertig = False
        st.session_state.checked = False
        st.rerun()

# -------------------- Fortschritt --------------------
st.sidebar.subheader("Fortschritt")

if st.sidebar.button("Anzeigen"):
    if st.session_state.user in progress:
        for eintrag in progress[st.session_state.user]:
            st.write(f"{eintrag['frage']} → {eintrag['deine_antwort']} (Lösung: {eintrag['lösung']})")
    else:
        st.info("Noch nichts gemacht")
