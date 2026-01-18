import streamlit as st
import random
import json
import os
from fractions import Fraction

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Lern-App", layout="centered")
st.markdown("## 🌈 📚 Lern-App für Kinder")

USERS_FILE = "users.json"
PROGRESS_FILE = "progress.json"

# ------------------ FILE HELPERS ------------------
def load_json(path, default):
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump(default, f)
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

users = load_json(USERS_FILE, {})
progress = load_json(PROGRESS_FILE, {})

# ------------------ SESSION STATE ------------------
if "user" not in st.session_state:
    st.session_state.user = None
if "mode" not in st.session_state:
    st.session_state.mode = "lernen"
if "quiz" not in st.session_state:
    st.session_state.quiz = []
if "index" not in st.session_state:
    st.session_state.index = 0
if "answer_key" not in st.session_state:
    st.session_state.answer_key = 0

# ------------------ LOGIN ------------------
if st.session_state.user is None:
    st.subheader("🔐 Login / Registrierung")

    u = st.text_input("Benutzername")
    p = st.text_input("Passwort", type="password")

    c1, c2 = st.columns(2)

    with c1:
        if st.button("Einloggen"):
            if u in users and users[u]["password"] == p:
                st.session_state.user = u
                st.success("✅ Eingeloggt")
                st.rerun()
            else:
                st.error("❌ Falsch")

    with c2:
        if st.button("Registrieren"):
            if u in users:
                st.error("❌ User existiert")
            else:
                users[u] = {"password": p}
                progress[u] = {}
                save_json(USERS_FILE, users)
                save_json(PROGRESS_FILE, progress)
                st.success("✅ Account erstellt")

    st.stop()

user = st.session_state.user

# ------------------ SIDEBAR ------------------
st.sidebar.markdown(f"👤 **{user}**")
if st.sidebar.button("🎮 Lernen"):
    st.session_state.mode = "lernen"
if st.sidebar.button("📊 Erledigt / Fortschritt"):
    st.session_state.mode = "fortschritt"
if st.sidebar.button("❌ Quiz abbrechen"):
    st.session_state.quiz = []
    st.session_state.index = 0

# ------------------ PROGRESS VIEW ------------------
if st.session_state.mode == "fortschritt":
    st.subheader("📊 Dein Fortschritt")

    user_data = progress.get(user, {})
    if not user_data:
        st.info("Noch keine Aufgaben gemacht 🙂")
    else:
        for fach, themen in user_data.items():
            st.markdown(f"### 📘 {fach}")
            for thema, stats in themen.items():
                st.success(
                    f"**{thema}** → Aufgaben: {stats['total']} | "
                    f"✅ {stats['richtig']} | ❌ {stats['falsch']}"
                )
    st.stop()

# ------------------ QUIZ GENERATION ------------------
def add_progress(fach, thema, richtig):
    progress.setdefault(user, {})
    progress[user].setdefault(fach, {})
    progress[user][fach].setdefault(thema, {"total": 0, "richtig": 0, "falsch": 0})

    progress[user][fach][thema]["total"] += 1
    if richtig:
        progress[user][fach][thema]["richtig"] += 1
    else:
        progress[user][fach][thema]["falsch"] += 1

    save_json(PROGRESS_FILE, progress)

# ------------------ LERNEN ------------------
st.subheader("🎯 Lernen")

fach = st.selectbox("Fach", ["Mathe", "Deutsch", "Englisch"])
themen = {
    "Mathe": ["Zufall", "Plus", "Minus", "Mal", "Geteilt", "Bruch", "Potenz"],
    "Deutsch": ["Plural", "Wortart", "Synonym"],
    "Englisch": ["Farben", "Vokabeln", "Verben"]
}
thema = st.selectbox("Thema", themen[fach])

if st.button("🧩 Aufgabe starten"):
    if fach == "Mathe":
        if thema == "Plus":
            a, b = random.randint(1, 50), random.randint(1, 50)
            st.session_state.quiz = [(f"{a} + {b}", a + b, f"{a}+{b}={a+b}")]
        elif thema == "Bruch":
            a, b = random.randint(1, 9), random.randint(1, 9)
            c, d = random.randint(1, 9), random.randint(1, 9)
            res = Fraction(a, b) + Fraction(c, d)
            st.session_state.quiz = [(f"{a}/{b} + {c}/{d}", str(res), f"{res}")]
        else:
            a, b = random.randint(2, 12), random.randint(2, 12)
            st.session_state.quiz = [(f"{a} × {b}", a * b, f"{a}×{b}={a*b}")]

    elif fach == "Deutsch":
        st.session_state.quiz = [("Plural von Hund", "Hunde", "Hund → Hunde")]

    else:
        st.session_state.quiz = [("Übersetze rot", "red", "rot = red")]

    st.session_state.index = 0
    st.session_state.answer_key += 1
    st.rerun()

# ------------------ QUIZ VIEW ------------------
if st.session_state.quiz:
    frage, lösung, erklärung = st.session_state.quiz[0]
    st.markdown(f"### ✏️ {frage}")

    antwort = st.text_input("Antwort", key=f"a{st.session_state.answer_key}")

    if st.button("✔️ Prüfen"):
        richtig = antwort.strip().lower() == str(lösung).lower()

        if richtig:
            st.success("✅ Richtig!")
        else:
            st.error("❌ Falsch")
            st.info(f"👉 {erklärung}")

        add_progress(fach, thema, richtig)
        st.session_state.quiz = []
        st.session_state.answer_key += 1
        st.rerun()
