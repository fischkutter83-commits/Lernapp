import streamlit as st
import random
import json
import os
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# ===================== GRUNDEINSTELLUNGEN ===================
# ============================================================

st.set_page_config(page_title="Lern-App", layout="wide")
st.title("📚 Lern-App")

USERS_FILE = "users.json"
PROGRESS_FILE = "progress.json"

# ============================================================
# ===================== JSON FUNKTIONEN ======================
# ============================================================

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

# ============================================================
# ===================== SESSION STATE ========================
# ============================================================

defaults = {
    "user": None,
    "aufgaben": [],
    "index": 0,
    "fertig": False,
    "show_points": False,
    "show_pie": False,
    "sterne": 0
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ============================================================
# ===================== LOGIN ================================
# ============================================================

if st.session_state.user is None:
    st.subheader("🔐 Login / Registrierung")

    col1, col2 = st.columns(2)
    with col1:
        username = st.text_input("Benutzername")
        password = st.text_input("Passwort", type="password")

        if st.button("Einloggen"):
            if username in users and users[username]["password"] == password:
                st.session_state.user = username
                st.session_state.sterne = users[username].get("sterne", 0)
                st.success("Willkommen 👋")
                st.rerun()
            else:
                st.error("Falsche Zugangsdaten")

    with col2:
        if st.button("Registrieren"):
            if username not in users:
                users[username] = {"password": password, "sterne": 0}
                save_json(USERS_FILE, users)
                st.success("Account erstellt – bitte einloggen")
            else:
                st.error("Benutzer existiert bereits")

    st.stop()

# ============================================================
# ===================== AUFGABENGENERATOREN ==================
# ============================================================

def unique_tasks(generator, count):
    seen = set()
    tasks = []
    while len(tasks) < count:
        q, a = generator()
        if q not in seen:
            seen.add(q)
            tasks.append((q, a))
    return tasks

def mathe_aufgaben(thema, klasse, anzahl):
    max_zahl = 20 if klasse <= 3 else 100 if klasse <= 6 else 500

    def gen():
        if thema == "Addition":
            a, b = random.randint(1, max_zahl), random.randint(1, max_zahl)
            return f"{a} + {b}", str(a + b)
        if thema == "Subtraktion":
            a, b = random.randint(10, max_zahl), random.randint(1, 10)
            return f"{a} - {b}", str(a - b)
        if thema == "Multiplikation":
            a, b = random.randint(2, 12), random.randint(2, 12)
            return f"{a} × {b}", str(a * b)
        if thema == "Division":
            b, r = random.randint(2, 10), random.randint(2, 10)
            return f"{b*r} ÷ {b}", str(r)
        if thema == "Potenzieren" and klasse >= 5:
            a, b = random.randint(2, 5), random.randint(2, 4)
            return f"{a}^{b}", str(a ** b)

    return unique_tasks(gen, anzahl)

def deutsch_aufgaben(thema, anzahl):
    pool = {
        "Rechtschreibung": {"Hant": "Hand", "Fahrrat": "Fahrrad", "Interresse": "Interesse"},
        "Artikel": {"___ Hund": "der", "___ Katze": "die", "___ Auto": "das"},
        "Satzglieder": {"Ich ___ den Ball": "werfe", "Der Hund ___ laut": "bellt"},
        "Wortarten": {"laufen": "Verb", "schön": "Adjektiv", "weil": "Konjunktion"}
    }

    def gen():
        q, a = random.choice(list(pool[thema].items()))
        return q, a

    return unique_tasks(gen, anzahl)

def englisch_aufgaben(thema, anzahl):
    pool = {
        "Vokabeln": {"Hund": "dog", "Katze": "cat", "Apfel": "apple"},
        "Zeitformen": {"I go (Past)": "went", "I see (Past)": "saw"}
    }

    def gen():
        q, a = random.choice(list(pool[thema].items()))
        return q, a

    return unique_tasks(gen, anzahl)

# ============================================================
# ===================== SIDEBAR ==============================
# ============================================================

st.sidebar.markdown("## ⚙️ Lern-Einstellungen")
st.sidebar.write(f"👤 **{st.session_state.user}**")
st.sidebar.markdown(f"⭐ **Sterne gesamt:** {st.session_state.sterne}")
st.sidebar.divider()

fach = st.sidebar.radio("📘 Fach", ["Mathe", "Deutsch", "Englisch"])
klasse = st.sidebar.slider("🎓 Klassenstufe", 1, 10, 3)

unterthemen = {
    "Mathe": ["Addition", "Subtraktion", "Multiplikation", "Division", "Potenzieren"],
    "Deutsch": ["Rechtschreibung", "Artikel", "Satzglieder", "Wortarten"],
    "Englisch": ["Vokabeln", "Zeitformen"]
}

thema = st.sidebar.selectbox("📂 Unterthema", unterthemen[fach])
anzahl = st.sidebar.slider("🧮 Anzahl Aufgaben", 1, 10, 5)

st.sidebar.divider()

if st.sidebar.button("🚀 Quiz starten", use_container_width=True):
    if fach == "Mathe":
        st.session_state.aufgaben = mathe_aufgaben(thema, klasse, anzahl)
    elif fach == "Deutsch":
        st.session_state.aufgaben = deutsch_aufgaben(thema, anzahl)
    else:
        st.session_state.aufgaben = englisch_aufgaben(thema, anzahl)

    st.session_state.index = 0
    st.session_state.fertig = False
    st.session_state.sterne_quiz = 0
    st.rerun()

if st.sidebar.button("📈 Punkte anzeigen", use_container_width=True):
    st.session_state.show_points = not st.session_state.show_points

if st.sidebar.button("📊 Lösungen anzeigen", use_container_width=True):
    st.session_state.show_pie = not st.session_state.show_pie

# ============================================================
# ===================== QUIZ ================================
# ============================================================

if st.session_state.aufgaben and not st.session_state.fertig:
    frage, loesung = st.session_state.aufgaben[st.session_state.index]

    st.subheader(f"📝 Aufgabe {st.session_state.index + 1}")
    st.markdown(f"### {frage}")
    st.markdown(f"⭐ **Sterne im Quiz:** {st.session_state.sterne_quiz}")

    antwort = st.text_input("Deine Antwort")

    if st.button("Antwort prüfen", use_container_width=True):
        richtig = antwort.strip().lower() == loesung.lower()

        if richtig:
            st.success("✅ Richtig! ⭐")
            st.session_state.sterne_quiz += 1
            st.session_state.sterne += 1
            users[st.session_state.user]["sterne"] = st.session_state.sterne
            save_json(USERS_FILE, users)
        else:
            st.error("❌ Falsch")

        progress.setdefault(st.session_state.user, []).append({
            "richtig": richtig
        })
        save_json(PROGRESS_FILE, progress)

    if st.button("➡️ Nächste Aufgabe", use_container_width=True):
        st.session_state.index += 1
        if st.session_state.index >= len(st.session_state.aufgaben):
            st.session_state.fertig = True
        st.rerun()

elif st.session_state.fertig:
    st.success(f"🎉 Quiz beendet – ⭐ {st.session_state.sterne_quiz} Sterne erhalten!")
    if st.button("🔁 Neues Quiz"):
        st.session_state.aufgaben = []
        st.session_state.fertig = False
        st.rerun()

# ============================================================
# ===================== DIAGRAMME ============================
# ============================================================

if st.session_state.show_points:
    st.markdown("---")
    st.header("📈 Gesamtpunkte")
    st.write(f"⭐ **Gesamtsterne:** {st.session_state.sterne}")

if st.session_state.show_pie:
    st.markdown("---")
    st.header("📊 Richtige vs. Falsche Antworten")

    daten = progress.get(st.session_state.user, [])
    if daten:
        richtig = sum(1 for d in daten if d["richtig"])
        falsch = sum(1 for d in daten if not d["richtig"])

        fig, ax = plt.subplots()
        ax.pie(
            [richtig, falsch],
            labels=["Richtig", "Falsch"],
            colors=["green", "red"],
            autopct="%1.0f%%",
            startangle=90
        )
        ax.axis("equal")
        st.pyplot(fig)
    else:
        st.info("Noch keine Daten vorhanden.")
