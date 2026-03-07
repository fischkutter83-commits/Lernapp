import streamlit as st
import random
import json
import os
import pandas as pd
import datetime

st.set_page_config(page_title="Lern-App", layout="wide")

USERS_FILE = "users.json"
PROGRESS_FILE = "progress.json"

# ================= JSON =================

def load_json(file):
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump({}, f)
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return {}

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

users = load_json(USERS_FILE)
progress = load_json(PROGRESS_FILE)

# ================= SESSION =================

defaults = {
    "user": None,
    "aufgaben": [],
    "index": 0,
    "fertig": False,
    "sterne": 0,
    "sterne_quiz": 0,
    "klasse": 3,
    "level": 1,
    "xp": 0,
    "spiel1": False,
    "spiel2": False,
    "spiel3": False,
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ================= LOGIN =================

if st.session_state.user is None:

    st.title("📚 Lern-App Login")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Login")

        username = st.text_input("Benutzername")
        password = st.text_input("Passwort", type="password")

        if st.button("Einloggen"):
            if username in users and users[username]["password"] == password:
                st.session_state.user = username
                st.session_state.sterne = users[username].get("sterne", 0)
                st.session_state.klasse = users[username].get("klasse", 3)
                st.session_state.level = users[username].get("level", 1)
                st.session_state.xp = users[username].get("xp", 0)
                st.rerun()
            else:
                st.error("Falsche Daten")

    with col2:
        st.subheader("Registrieren")

        new_user = st.text_input("Neuer Benutzername")
        new_pw = st.text_input("Neues Passwort", type="password")

        if st.button("Account erstellen"):
            if new_user not in users:
                users[new_user] = {"password": new_pw, "sterne": 0, "klasse": 3, "level":1, "xp":0}
                save_json(USERS_FILE, users)
                st.success("Account erstellt")
            else:
                st.error("Benutzer existiert bereits")

    st.stop()

# ================= TOP BAR =================

col1, col2, col3, col4 = st.columns([3,1,1,1])

with col1:
    st.title("📚 Lern-App")

with col2:
    st.metric("⭐ Sterne", st.session_state.sterne)

with col3:
    st.metric("🏆 Level", st.session_state.level)

with col4:
    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()

# ================= LEVEL SYSTEM =================

def add_xp(amount):
    st.session_state.xp += amount
    if st.session_state.xp >= 10:
        st.session_state.level += 1
        st.session_state.xp = 0
        st.success("🎉 Level Up!")

# ================= KLASSENSTUFE =================

st.session_state.klasse = st.slider("🎓 Klassenstufe", 1, 10, st.session_state.klasse)

# ================= AUFGABEN =================

def mathe_aufgaben(thema, klasse, anzahl):
    max_zahl = 20 if klasse <= 3 else 100 if klasse <= 6 else 500
    tasks = []
    for _ in range(anzahl):
        if thema == "Addition":
            a = random.randint(1, max_zahl)
            b = random.randint(1, max_zahl)
            tasks.append((f"{a} + {b}", str(a + b)))
        if thema == "Subtraktion":
            a = random.randint(1, max_zahl)
            b = random.randint(1, max_zahl)
            tasks.append((f"{a} - {b}", str(a - b)))
        if thema == "Multiplikation":
            a = random.randint(2, 12)
            b = random.randint(2, 12)
            tasks.append((f"{a} × {b}", str(a * b)))
    return tasks

def deutsch_aufgaben(thema, klasse, anzahl):
    daten = {
        "Artikel": {"___ Hund":"der","___ Katze":"die","___ Auto":"das"},
        "Wortarten": {"laufen":"Verb","Haus":"Nomen","schnell":"Adjektiv"},
        "Grammatik": {"Ich ___ zur Schule":"gehe","Wir ___ Fußball":"spielen"},
        "Zeitformen": {"ich gehe (Vergangenheit)":"ging","ich esse (Vergangenheit)":"aß"}
    }
    pool = list(daten[thema].items())
    random.shuffle(pool)
    return pool[:anzahl]

def englisch_aufgaben(thema, klasse, anzahl):
    daten = {
        "Vocabulary":{"Hund":"dog","Katze":"cat","Haus":"house"},
        "Grammar":{"I ___ fast":"run","She ___ fast":"runs"},
        "Tenses":{"go (past)":"went","see (past)":"saw"}
    }
    pool = list(daten[thema].items())
    random.shuffle(pool)
    return pool[:anzahl]

# ================= EINSTELLUNGEN =================

st.subheader("⚙️ Einstellungen")

col1, col2, col3 = st.columns(3)

with col1:
    fach = st.selectbox("Fach", ["Mathe", "Deutsch", "Englisch"])

with col2:
    themen = {
        "Mathe": ["Addition", "Subtraktion", "Multiplikation"],
        "Deutsch": ["Grammatik", "Zeitformen", "Artikel", "Wortarten"],
        "Englisch": ["Tenses", "Grammar", "Vocabulary"],
    }
    thema = st.selectbox("Thema", themen[fach])

with col3:
    anzahl = st.slider("Aufgaben", 1, 10, 5)

if st.button("🚀 Quiz starten"):
    if fach == "Mathe":
        st.session_state.aufgaben = mathe_aufgaben(thema, st.session_state.klasse, anzahl)
    elif fach == "Deutsch":
        st.session_state.aufgaben = deutsch_aufgaben(thema, st.session_state.klasse, anzahl)
    else:
        st.session_state.aufgaben = englisch_aufgaben(thema, st.session_state.klasse, anzahl)

    st.session_state.index = 0
    st.session_state.fertig = False
    st.session_state.sterne_quiz = 0

# ================= QUIZ =================

if st.session_state.aufgaben and not st.session_state.fertig:

    frage, loesung = st.session_state.aufgaben[st.session_state.index]

    st.subheader(f"Aufgabe {st.session_state.index+1}")
    st.write(f"### {frage}")

    antwort = st.text_input("Antwort")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Antwort prüfen"):
            if antwort.lower() == loesung.lower():
                st.success("Richtig ⭐")
                st.session_state.sterne += 1
                st.session_state.sterne_quiz += 1
                add_xp(2)
            else:
                st.error(f"Falsch! Richtige Antwort: {loesung}")

    with col2:
        if st.button("Nächste"):
            st.session_state.index += 1
            if st.session_state.index >= len(st.session_state.aufgaben):
                st.session_state.fertig = True

# ================= QUIZENDE =================

if st.session_state.fertig:

    st.success(f"Quiz beendet ⭐ {st.session_state.sterne_quiz}")

    date = str(datetime.date.today())

    if st.session_state.user not in progress:
        progress[st.session_state.user] = {}

    progress[st.session_state.user][date] = st.session_state.sterne_quiz

    save_json(PROGRESS_FILE, progress)

# ================= FORTSCHRITT =================

st.subheader("📈 Lernfortschritt")

if st.session_state.user in progress:

    data = progress[st.session_state.user]

    df = pd.DataFrame(list(data.items()), columns=["Datum", "Sterne"])

    col_chart, col_space = st.columns([1,2])

    with col_chart:
        st.line_chart(df.set_index("Datum"))

# ================= SPIELE SHOP =================

st.subheader("🎮 Spiele-Shop")

col1, col2, col3 = st.columns(3)

with col1:
    st.write("🎯 Zahlen raten")
    if not st.session_state.spiel1:
        if st.button("Kaufen ⭐10"):
            if st.session_state.sterne >= 10:
                st.session_state.sterne -= 10
                st.session_state.spiel1 = True

with col2:
    st.write("🎲 Würfelspiel")
    if not st.session_state.spiel2:
        if st.button("Kaufen ⭐15"):
            if st.session_state.sterne >= 15:
                st.session_state.sterne -= 15
                st.session_state.spiel2 = True

with col3:
    st.write("🧠 Reaktionsspiel")
    if not st.session_state.spiel3:
        if st.button("Kaufen ⭐20"):
            if st.session_state.sterne >= 20:
                st.session_state.sterne -= 20
                st.session_state.spiel3 = True

# ================= SPIEL 1 =================

if st.session_state.spiel1:

    st.subheader("🎯 Zahlen raten")

    if "zahl" not in st.session_state:
        st.session_state.zahl = random.randint(1, 20)

    guess = st.number_input("Rate die Zahl 1-20", 1, 20)

    if st.button("Raten"):

        if guess == st.session_state.zahl:
            st.success("Richtig +2⭐")
            st.session_state.sterne += 2
            st.session_state.zahl = random.randint(1, 20)

        elif guess < st.session_state.zahl:
            st.info("Zu klein")

        else:
            st.info("Zu groß")

# ================= SPIEL 2 =================

if st.session_state.spiel2:

    st.subheader("🎲 Würfelspiel")

    if st.button("Würfeln"):

        roll = random.randint(1,6)

        st.write("Du hast gewürfelt:", roll)

        if roll == 6:
            st.success("Jackpot +3⭐")
            st.session_state.sterne += 3

# ================= SPIEL 3 =================

if st.session_state.spiel3:

    st.subheader("⚡ Reaktionsspiel")

    if st.button("Start"):

        number = random.randint(1,5)

        guess = st.number_input("Drücke schnell die Zahl",1,5)

        if guess == number:
            st.success("Schnell! +4⭐")
            st.session_state.sterne += 4
