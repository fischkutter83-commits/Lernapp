import streamlit as st
import random
import json
import os
import hashlib

# -------------------- Design --------------------
st.set_page_config(page_title="Lern-App", layout="centered")
st.markdown("""
<style>
    .main {background-color: #f7f9fc;}
    h1, h2, h3 {color: #2c3e50;}
</style>
""", unsafe_allow_html=True)

st.title("📚 Lern-App")

# -------------------- Dateien --------------------
USERS_FILE = "users.json"
PROGRESS_FILE = "progress.json"

# -------------------- Helper --------------------
def load(file):
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump({}, f)
    with open(file, "r") as f:
        return json.load(f)

def save(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

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

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Einloggen"):
            if u in users and users[u] == hash_pw(p):
                st.session_state.user = u
                st.experimental_rerun()
            else:
                st.error("❌ Falsche Daten")

    with col2:
        if st.button("Registrieren"):
            if u in users:
                st.error("❌ Benutzer existiert bereits")
            else:
                users[u] = hash_pw(p)
                save(USERS_FILE, users)
                st.success("✅ Account erstellt")

    st.stop()

# -------------------- Aufgaben --------------------
def mathe(n):
    out = []
    for _ in range(n):
        a, b = random.randint(1, 10), random.randint(1, 10)
        out.append((f"{a} + {b}", str(a + b)))
    return out

def englisch(n):
    w = {"rot": "red", "blau": "blue", "Hund": "dog", "Katze": "cat"}
    return [(f"Übersetze: {k}", v) for k, v in random.sample(list(w.items()), n)]

# -------------------- Sidebar --------------------
st.sidebar.success(f"👤 {st.session_state.user}")
fach = st.sidebar.selectbox("📘 Fach", ["Mathe", "Englisch"])
anzahl = st.sidebar.slider("🧩 Aufgaben", 1, 5, 3)

if st.sidebar.button("▶️ Quiz starten"):
    st.session_state.tasks = mathe(anzahl) if fach == "Mathe" else englisch(anzahl)
    st.session_state.i = 0
    st.session_state.done = False
    st.experimental_rerun()

# -------------------- Quiz --------------------
if st.session_state.tasks and not st.session_state.done:
    frage, loesung = st.session_state.tasks[st.session_state.i]

    st.subheader(f"Aufgabe {st.session_state.i + 1}")
    st.write(frage)

    answer = st.text_input("Deine Antwort", key=f"a_{st.session_state.i}")

    if st.button("Antwort prüfen", key=f"check_{st.session_state.i}"):
        richtig = answer.strip().lower() == loesung.lower()
        st.success("✅ Richtig!") if richtig else st.error(f"❌ Falsch → {loesung}")

        progress.setdefault(st.session_state.user, []).append({
            "fach": fach,
            "richtig": richtig
        })
        save(PROGRESS_FILE, progress)

    if st.button("➡️ Weiter", key=f"next_{st.session_state.i}"):
        st.session_state.i += 1
        if st.session_state.i >= len(st.session_state.tasks):
            st.session_state.done = True
        st.experimental_rerun()

elif st.session_state.done:
    st.success("🎉 Quiz abgeschlossen!")
    if st.button("🔁 Neues Quiz"):
        st.session_state.tasks = []
        st.session_state.done = False
        st.experimental_rerun()

# -------------------- Statistiken --------------------
st.sidebar.subheader("📊 Statistik")

if st.sidebar.button("Anzeigen"):
    daten = progress.get(st.session_state.user, [])
    if not daten:
        st.info("Noch keine Daten")
    else:
        richtig = sum(1 for d in daten if d["richtig"])
        falsch = len(daten) - richtig

        st.metric("✅ Richtig", richtig)
        st.metric("❌ Falsch", falsch)

        mathe_r = sum(1 for d in daten if d["fach"] == "Mathe" and d["richtig"])
        eng_r = sum(1 for d in daten if d["fach"] == "Englisch" and d["richtig"])

        st.write("**Pro Fach:**")
        st.write(f"Mathe richtig: {mathe_r}")
        st.write(f"Englisch richtig: {eng_r}")
