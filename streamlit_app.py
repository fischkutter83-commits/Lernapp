import streamlit as st
import random
import json
import os

# -------------------- Grundeinstellungen --------------------
st.set_page_config(
    page_title="Lern-App",
    layout="wide"
)

st.title("📚 Lern-App")

USERS_FILE = "users.json"
PROGRESS_FILE = "progress.json"

# -------------------- JSON laden / speichern --------------------
def load_json(file):
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump({}, f)
    with open(file, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

users = load_json(USERS_FILE)
progress = load_json(PROGRESS_FILE)

# -------------------- Session State --------------------
defaults = {
    "user": None,
    "aufgaben": [],
    "index": 0,
    "fertig": False
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# -------------------- LOGIN --------------------
if st.session_state.user is None:
    st.subheader("🔐 Login / Registrierung")

    col1, col2 = st.columns(2)
    with col1:
        username = st.text_input("Benutzername")
        password = st.text_input("Passwort", type="password")

        if st.button("Einloggen"):
            if username in users and users[username]["password"] == password:
                st.session_state.user = username
                st.success("Willkommen 👋")
                st.rerun()
            else:
                st.error("Falsche Zugangsdaten")

    with col2:
        if st.button("Registrieren"):
            if username in users:
                st.error("Benutzer existiert bereits")
            else:
                users[username] = {"password": password}
                save_json(USERS_FILE, users)
                st.success("Account erstellt – bitte einloggen")

    st.stop()

# ============================================================
# ===================== AUFGABENGENERATOREN ==================
# ============================================================

def mathe_aufgaben(thema, anzahl):
    a = []
    for _ in range(anzahl):
        if thema == "Addition":
            x, y = random.randint(1, 50), random.randint(1, 50)
            a.append((f"{x} + {y}", str(x + y)))
        elif thema == "Subtraktion":
            x, y = random.randint(20, 50), random.randint(1, 20)
            a.append((f"{x} - {y}", str(x - y)))
        elif thema == "Multiplikation":
            x, y = random.randint(2, 12), random.randint(2, 12)
            a.append((f"{x} × {y}", str(x * y)))
        elif thema == "Division":
            y = random.randint(2, 12)
            r = random.randint(2, 12)
            a.append((f"{y*r} ÷ {y}", str(r)))
        elif thema == "Potenzieren":
            x, y = random.randint(2, 6), random.randint(2, 4)
            a.append((f"{x}^{y}", str(x ** y)))
    return a

def deutsch_aufgaben(thema, anzahl):
    daten = {
        "Rechtschreibung": {"Hant": "Hand", "Hauß": "Haus"},
        "Artikel": {"___ Hund": "der", "___ Katze": "die"},
        "Satzglieder": {"Ich ___ den Ball": "werfe"},
        "Wortarten": {"laufen": "Verb", "Haus": "Nomen"}
    }
    a = []
    for _ in range(anzahl):
        f, l = random.choice(list(daten[thema].items()))
        a.append((f, l))
    return a

def englisch_aufgaben(thema, anzahl):
    daten = {
        "Vokabeln": {"Hund": "dog", "Katze": "cat"},
        "Zeitformen": {"I go (Past)": "went", "I see (Past)": "saw"}
    }
    a = []
    for _ in range(anzahl):
        f, l = random.choice(list(daten[thema].items()))
        a.append((f, l))
    return a

# ============================================================
# ======================== SIDEBAR ===========================
# ============================================================

st.sidebar.header("⚙️ Einstellungen")
st.sidebar.write(f"👤 {st.session_state.user}")

fach = st.sidebar.radio(
    "Fach wählen",
    ["Mathe", "Deutsch", "Englisch"]
)

unterthemen = {
    "Mathe": ["Addition", "Subtraktion", "Multiplikation", "Division", "Potenzieren"],
    "Deutsch": ["Rechtschreibung", "Artikel", "Satzglieder", "Wortarten"],
    "Englisch": ["Vokabeln", "Zeitformen"]
}

thema = st.sidebar.selectbox("Unterthema", unterthemen[fach])
anzahl = st.sidebar.slider("Anzahl Aufgaben", 1, 10, 5)

if st.sidebar.button("🚀 Quiz starten"):
    if fach == "Mathe":
        st.session_state.aufgaben = mathe_aufgaben(thema, anzahl)
    elif fach == "Deutsch":
        st.session_state.aufgaben = deutsch_aufgaben(thema, anzahl)
    else:
        st.session_state.aufgaben = englisch_aufgaben(thema, anzahl)

    st.session_state.index = 0
    st.session_state.fertig = False
    st.rerun()

# ============================================================
# ======================== QUIZ ==============================
# ============================================================

if st.session_state.aufgaben and not st.session_state.fertig:
    frage, loesung = st.session_state.aufgaben[st.session_state.index]

    st.subheader(f"📝 Aufgabe {st.session_state.index + 1}")
    st.markdown(f"### {frage}")

    antwort = st.text_input("Deine Antwort")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Antwort prüfen"):
            if antwort.strip().lower() == loesung.lower():
                st.success("Richtig ✅")
            else:
                st.error(f"Falsch ❌ – Lösung: {loesung}")

            progress.setdefault(st.session_state.user, []).append({
                "fach": fach,
                "thema": thema,
                "frage": frage,
                "antwort": antwort,
                "lösung": loesung
            })
            save_json(PROGRESS_FILE, progress)

    with col2:
        if st.button("Nächste Aufgabe ➡️"):
            st.session_state.index += 1
            if st.session_state.index >= len(st.session_state.aufgaben):
                st.session_state.fertig = True
            st.rerun()

elif st.session_state.fertig:
    st.success("🎉 Quiz abgeschlossen!")
    if st.button("🔁 Neues Quiz"):
        st.session_state.aufgaben = []
        st.session_state.fertig = False
        st.rerun()
