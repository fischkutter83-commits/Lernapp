import streamlit as st
import random
import json
import os

# -------------------- Grundeinstellungen --------------------
st.set_page_config(page_title="Lern-App", layout="centered")
st.title("📚 Lern-App")

USERS_FILE = "users.json"
PROGRESS_FILE = "progress.json"

# -------------------- JSON-Funktionen --------------------
def load_json(file):
    if not os.path.exists(file):
        with open(file, "w", encoding="utf-8") as f:
            json.dump({}, f)
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

users = load_json(USERS_FILE)
progress = load_json(PROGRESS_FILE)

# -------------------- Session State --------------------
st.session_state.setdefault("user", None)
st.session_state.setdefault("aufgaben", [])
st.session_state.setdefault("index", 0)
st.session_state.setdefault("fertig", False)
st.session_state.setdefault("antwort_geprüft", False)

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
                st.experimental_rerun()
            else:
                st.error("❌ Benutzername oder Passwort falsch")

    with col2:
        if st.button("Registrieren"):
            if username in users:
                st.error("❌ Benutzer existiert bereits")
            else:
                users[username] = {"password": password}
                save_json(USERS_FILE, users)
                st.success("✅ Account erstellt")

    st.stop()

# -------------------- Aufgaben --------------------
def generiere_mathe_aufgaben(anzahl):
    aufgaben = []
    for _ in range(anzahl):
        a, b = random.randint(1, 20), random.randint(1, 20)
        aufgaben.append((f"{a} + {b}", str(a + b), f"{a} + {b} = {a + b}"))
    return aufgaben

def generiere_englisch_aufgaben(anzahl):
    vokabeln = {
        "rot": "red",
        "blau": "blue",
        "Hund": "dog"
    }
    anzahl = min(anzahl, len(vokabeln))  # 🔴 WICHTIGER BUGFIX
    return [
        (f"Übersetze: {k}", v, f"{k} = {v}")
        for k, v in random.sample(list(vokabeln.items()), anzahl)
    ]

# -------------------- Menü --------------------
st.sidebar.write(f"👤 {st.session_state.user}")

fach = st.sidebar.radio("Fach", ["Mathe", "Englisch"])

max_anzahl = 5 if fach == "Mathe" else 3
anzahl = st.sidebar.slider("Aufgaben", 1, max_anzahl, 3)

if st.sidebar.button("Quiz starten"):
    st.session_state.aufgaben = (
        generiere_mathe_aufgaben(anzahl)
        if fach == "Mathe"
        else generiere_englisch_aufgaben(anzahl)
    )
    st.session_state.index = 0
    st.session_state.fertig = False
    st.session_state.antwort_geprüft = False
    st.experimental_rerun()

# -------------------- Quiz --------------------
if st.session_state.aufgaben and not st.session_state.fertig:
    idx = st.session_state.index
    frage, loesung, erklaerung = st.session_state.aufgaben[idx]

    st.subheader(f"Aufgabe {idx + 1}")
    st.write(frage)

    answer_key = f"antwort_{idx}"
    st.text_input("Deine Antwort", key=answer_key)

    if st.button("Antwort prüfen") and not st.session_state.antwort_geprüft:
        user_answer = st.session_state[answer_key].strip().lower()

        if user_answer == loesung.lower():
            st.success("✅ Richtig!")
        else:
            st.error("❌ Falsch")
            st.info(erklaerung)

        progress.setdefault(st.session_state.user, []).append({
            "fach": fach,
            "frage": frage,
            "antwort": user_answer,
            "loesung": loesung
        })
        save_json(PROGRESS_FILE, progress)

        st.session_state.antwort_geprüft = True

    if st.session_state.antwort_geprüft:
        if st.button("Nächste Aufgabe"):
            st.session_state.index += 1
            st.session_state.antwort_geprüft = False
            if st.session_state.index >= len(st.session_state.aufgaben):
                st.session_state.fertig = True
            st.experimental_rerun()

elif st.session_state.fertig:
    st.success("🎉 Quiz beendet!")
    if st.button("Nochmal spielen"):
        st.session_state.aufgaben = []
        st.session_state.fertig = False
        st.experimental_rerun()

# -------------------- Fortschritt --------------------
st.sidebar.subheader("📊 Fortschritt")
if st.sidebar.button("Anzeigen"):
    einträge = progress.get(st.session_state.user, [])
    if not einträge:
        st.sidebar.info("Noch keine Einträge")
    for e in einträge:
        st.sidebar.write(f"{e['fach']} | {e['frage']} → {e['loesung']}")
