import streamlit as st
import random
import json
import os
from datetime import datetime

# ================== GRUNDEINSTELLUNGEN ==================
st.set_page_config(page_title="🎓 Lern-App", layout="centered")

st.markdown("""
<style>
.big-button button {
    font-size: 22px !important;
    padding: 15px !important;
}
.card {
    background-color: #f0f8ff;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

st.title("📚 Bunte Lern-App")

USERS_FILE = "users.json"
HISTORY_FILE = "history.json"

# ================== DATEIEN ==================
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
history = load_json(HISTORY_FILE, {})

# ================== SESSION STATE ==================
defaults = {
    "user": None,
    "aufgaben": [],
    "index": 0,
    "punkte": 0,
    "fertig": False,
    "antworten": [],
    "quiz_aktiv": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ================== LOGIN ==================
if st.session_state.user is None:
    st.subheader("🔐 Login / Registrierung")
    username = st.text_input("👤 Benutzername")
    password = st.text_input("🔑 Passwort", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Einloggen"):
            if username in users and users[username] == password:
                st.session_state.user = username
                st.rerun()
            else:
                st.error("❌ Falsch")

    with col2:
        if st.button("Registrieren"):
            if username in users:
                st.error("❌ Benutzer existiert")
            else:
                users[username] = password
                save_json(USERS_FILE, users)
                st.success("✅ Account erstellt")

    st.stop()

# ================== AUFGABEN ==================
def mathe_aufgabe(thema):
    if thema == "Plus":
        a, b = random.randint(1, 50), random.randint(1, 50)
        return f"{a} + {b}", a + b, f"{a} + {b} = {a+b}"
    if thema == "Minus":
        a, b = random.randint(20, 50), random.randint(1, 20)
        return f"{a} - {b}", a - b, f"{a} - {b} = {a-b}"
    if thema == "Mal":
        a, b = random.randint(2, 12), random.randint(2, 12)
        return f"{a} × {b}", a * b, f"{a} × {b} = {a*b}"

def deutsch_aufgabe():
    w = {"Hund": "Hunde", "Katze": "Katzen"}
    wort, lösung = random.choice(list(w.items()))
    return f"Plural von {wort}", lösung, f"{wort} → {lösung}"

def englisch_aufgabe():
    w = {"Hund": "dog", "Katze": "cat"}
    de, en = random.choice(list(w.items()))
    return f"Übersetze: {de}", en, f"{de} = {en}"

# ================== SIDEBAR ==================
st.sidebar.markdown(f"👤 **{st.session_state.user}**")

fach = st.sidebar.radio("📘 Fach", ["Mathe", "Deutsch", "Englisch"])

modus = st.sidebar.radio("🎯 Modus", ["Zufall", "Thema wählen"])

if fach == "Mathe" and modus == "Thema wählen":
    thema = st.sidebar.selectbox("🧮 Thema", ["Plus", "Minus", "Mal"])
else:
    thema = None

anzahl = st.sidebar.slider("📌 Aufgaben", 1, 10, 5)

if st.sidebar.button("🚀 Quiz starten"):
    st.session_state.aufgaben = []
    st.session_state.antworten = []
    st.session_state.index = 0
    st.session_state.punkte = 0
    st.session_state.fertig = False
    st.session_state.quiz_aktiv = True

    for _ in range(anzahl):
        if fach == "Mathe":
            t = thema if thema else random.choice(["Plus", "Minus", "Mal"])
            st.session_state.aufgaben.append(mathe_aufgabe(t))
        elif fach == "Deutsch":
            st.session_state.aufgaben.append(deutsch_aufgabe())
        else:
            st.session_state.aufgaben.append(englisch_aufgabe())

    st.rerun()

if st.sidebar.button("🛑 Abbrechen"):
    st.session_state.quiz_aktiv = False
    st.session_state.aufgaben = []
    st.rerun()

# ================== QUIZ ==================
if st.session_state.quiz_aktiv and not st.session_state.fertig:
    if st.session_state.index >= len(st.session_state.aufgaben):
        st.session_state.fertig = True
        st.rerun()

    frage, lösung, erklärung = st.session_state.aufgaben[st.session_state.index]

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader(f"📝 Aufgabe {st.session_state.index + 1}")
    st.write(frage)
    antwort = st.text_input("✏️ Deine Antwort")

    if st.button("✅ Prüfen"):
        richtig = antwort.strip().lower() == str(lösung).lower()

        st.session_state.antworten.append({
            "frage": frage,
            "antwort": antwort,
            "lösung": str(lösung),
            "richtig": richtig,
            "erklärung": erklärung
        })

        if richtig:
            st.success("🎉 Richtig!")
            st.session_state.punkte += 1
        else:
            st.error("❌ Falsch")
            st.info(erklärung)

        st.session_state.index += 1
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ================== ERGEBNIS ==================
if st.session_state.fertig:
    st.balloons()
    st.success(f"🏆 Punkte: {st.session_state.punkte}/{len(st.session_state.aufgaben)}")

    history.setdefault(st.session_state.user, []).append({
        "datum": datetime.now().strftime("%d.%m.%Y %H:%M"),
        "ergebnisse": st.session_state.antworten
    })
    save_json(HISTORY_FILE, history)

    if st.button("🔁 Neues Quiz"):
        st.session_state.quiz_aktiv = False
        st.session_state.fertig = False
        st.rerun()

# ================== VERLAUF ==================
st.subheader("📜 Meine Aufgaben")

for eintrag in history.get(st.session_state.user, []):
    with st.expander(eintrag["datum"]):
        for a in eintrag["ergebnisse"]:
            icon = "✅" if a["richtig"] else "❌"
            st.write(f"{icon} {a['frage']}")
            if not a["richtig"]:
                st.caption(f"➡️ Richtig: {a['lösung']}")
