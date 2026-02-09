import streamlit as st
import random
import json
import os
from fractions import Fraction

# -------------------- Setup --------------------
st.set_page_config(page_title="Lern-App", layout="centered")
st.title("📚 Lern-App")

USERS_FILE = "users.json"
PROGRESS_FILE = "progress.json"

# -------------------- Helper --------------------
def load(file):
    if not os.path.exists(file):
        with open(file, "w", encoding="utf-8") as f:
            json.dump({}, f)
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)

def save(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

users = load(USERS_FILE)
progress = load(PROGRESS_FILE)

# -------------------- Session --------------------
st.session_state.setdefault("user", None)
st.session_state.setdefault("tasks", [])
st.session_state.setdefault("i", 0)
st.session_state.setdefault("done", False)

# -------------------- Login --------------------
if st.session_state.user is None:
    st.subheader("🔐 Login / Registrierung")
    u = st.text_input("Benutzername")
    p = st.text_input("Passwort", type="password")

    if st.button("Einloggen"):
        if u in users and users[u] == p:
            st.session_state.user = u
            st.experimental_rerun()
        else:
            st.error("Falsche Daten")

    if st.button("Registrieren"):
        if u in users:
            st.error("Benutzer existiert")
        else:
            users[u] = p
            save(USERS_FILE, users)
            st.success("Account erstellt")

    st.stop()

# -------------------- Aufgaben --------------------
def mathe(klasse, n):
    out = []
    for _ in range(n):
        a, b = random.randint(1, 10), random.randint(1, 10)
        out.append((f"{a} + {b}", str(a + b)))
    return out

def deutsch(_, n):
    w = {"Hund": "Hunde", "Katze": "Katzen"}
    return [(f"Plural von {k}", v) for k, v in random.sample(list(w.items()), n)]

def englisch(_, n):
    w = {"rot": "red", "blau": "blue"}
    return [(f"Übersetze {k}", v) for k, v in random.sample(list(w.items()), n)]

# -------------------- Menü --------------------
st.sidebar.write(f"👤 {st.session_state.user}")
fach = st.sidebar.selectbox("Fach", ["Mathe", "Deutsch", "Englisch"])
klasse = st.sidebar.slider("Klasse", 1, 10, 1)
anzahl = st.sidebar.slider("Aufgaben", 1, 5, 3)

if st.sidebar.button("Quiz starten"):
    if fach == "Mathe":
        st.session_state.tasks = mathe(klasse, anzahl)
    elif fach == "Deutsch":
        st.session_state.tasks = deutsch(klasse, anzahl)
    else:
        st.session_state.tasks = englisch(klasse, anzahl)

    st.session_state.i = 0
    st.session_state.done = False
    st.experimental_rerun()

# -------------------- Quiz --------------------
if st.session_state.tasks and not st.session_state.done:
    frage, loesung = st.session_state.tasks[st.session_state.i]
    st.subheader(f"Aufgabe {st.session_state.i + 1}")
    st.write(frage)

    answer = st.text_input("Antwort", key=f"a_{st.session_state.i}")

    if st.button("Prüfen", key=f"check_{st.session_state.i}"):
        if answer.strip().lower() == loesung.lower():
            st.success("Richtig ✅")
        else:
            st.error(f"Falsch ❌ → {loesung}")

        progress.setdefault(st.session_state.user, []).append({
            "fach": fach,
            "frage": frage,
            "antwort": answer,
            "lösung": loesung
        })
        save(PROGRESS_FILE, progress)

    if st.button("Weiter", key=f"next_{st.session_state.i}"):
        st.session_state.i += 1
        if st.session_state.i >= len(st.session_state.tasks):
            st.session_state.done = True
        st.experimental_rerun()

elif st.session_state.done:
    st.success("🎉 Fertig!")
    if st.button("Nochmal"):
        st.session_state.tasks = []
        st.session_state.done = False
        st.experimental_rerun()

# -------------------- Fortschritt --------------------
st.sidebar.subheader("📊 Fortschritt")
if st.sidebar.button("Anzeigen"):
    for e in progress.get(st.session_state.user, []):
        st.write(f"{e['fach']} | {e['frage']} → {e['lösung']}")
