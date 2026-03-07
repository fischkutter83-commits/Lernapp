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
                st.session_state.spiel1 = users[username].get("spiel1", False)
                st.session_state.spiel2 = users[username].get("spiel2", False)
                st.session_state.spiel3 = users[username].get("spiel3", False)
                st.rerun()
            else:
                st.error("Falsche Daten")
    with col2:
        st.subheader("Registrieren")
        new_user = st.text_input("Neuer Benutzername")
        new_pw = st.text_input("Neues Passwort", type="password")
        if st.button("Account erstellen"):
            if new_user not in users:
                users[new_user] = {
                    "password": new_pw,
                    "sterne": 0,
                    "klasse": 3,
                    "level":1,
                    "xp":0,
                    "spiel1": False,
                    "spiel2": False,
                    "spiel3": False
                }
                save_json(USERS_FILE, users)
                st.success("Account erstellt")
            else:
                st.error("Benutzer existiert bereits")
    st.stop()

# ================= TOP BAR =================
col1, col2, col3, col4 = st.columns([3,1,1,1])
with col1: st.title("📚 Lern-App")
with col2: st.metric("⭐ Sterne", st.session_state.sterne)
with col3: st.metric("🏆 Level", st.session_state.level)
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
    # Fortschritt in users.json speichern
    users[st.session_state.user]["xp"] = st.session_state.xp
    users[st.session_state.user]["level"] = st.session_state.level
    save_json(USERS_FILE, users)

# ================= KLASSENSTUFE =================
st.session_state.klasse = st.slider("🎓 Klassenstufe", 1, 10, st.session_state.klasse)
users[st.session_state.user]["klasse"] = st.session_state.klasse
save_json(USERS_FILE, users)

# ================= AUFGABEN =================
def mathe_aufgaben(thema, klasse, anzahl):
    tasks = []
    for _ in range(anzahl):
        if thema == "Addition":
            max_zahl = 10*klasse if klasse <=5 else 50*klasse
            a = random.randint(1, max_zahl)
            b = random.randint(1, max_zahl)
            frage = f"Was ist {a} plus {b}?"
            tasks.append((frage, str(a+b)))
        elif thema == "Subtraktion":
            max_zahl = 10*klasse if klasse <=5 else 50*klasse
            a = random.randint(1, max_zahl)
            b = random.randint(1, a)
            frage = f"Berechne {a} minus {b}."
            tasks.append((frage, str(a-b)))
        elif thema == "Multiplikation" and klasse >= 2:
            a = random.randint(2, 5 + klasse)
            b = random.randint(2, 5 + klasse)
            frage = f"Wie viel ist {a} mal {b}?"
            tasks.append((frage, str(a*b)))
    return tasks

def deutsch_aufgaben(thema, klasse, anzahl):
    daten = {
        "Artikel": {f"Fülle ein: ___ Hund":"der","Fülle ein: ___ Katze":"die","Fülle ein: ___ Auto":"das",
                    "Fülle ein: ___ Baum":"der","Fülle ein: ___ Blume":"die"},
        "Wortarten": {"Bestimme die Wortart: laufen":"Verb","Bestimme die Wortart: Haus":"Nomen","Bestimme die Wortart: schnell":"Adjektiv",
                      "Bestimme die Wortart: spielen":"Verb","Bestimme die Wortart: schön":"Adjektiv"},
        "Grammatik": {"Setze ein: Ich ___ zur Schule":"gehe","Setze ein: Wir ___ Fußball":"spielen","Setze ein: Er ___ im Garten":"arbeitet"},
        "Zeitformen": {"Schreibe in Vergangenheit: ich gehe":"ging","Schreibe in Vergangenheit: ich esse":"aß",
                       "Schreibe in Vergangenheit: wir spielen":"spielten"}
    }
    pool = list(daten[thema].items())
    random.shuffle(pool)
    return pool[:anzahl]

def englisch_aufgaben(thema, klasse, anzahl):
    daten = {
        "Vocabulary":{"Translate to English: Hund":"dog","Translate to English: Katze":"cat","Translate to English: Haus":"house",
                      "Translate to English: Baum":"tree","Translate to English: Blume":"flower"},
        "Grammar":{"Fill in: I ___ fast":"run","Fill in: She ___ fast":"runs","Fill in: They ___ happy":"are"},
        "Tenses":{"Write past tense: go":"went","Write past tense: see":"saw","Write past tense: eat":"ate"}
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
    antwort = st.text_input("Antwort", key=f"antwort_{st.session_state.index}")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Antwort prüfen", key=f"check_{st.session_state.index}"):
            if antwort.strip().lower() == loesung.lower():
                st.success("Richtig ⭐")
                st.session_state.sterne += 1
                st.session_state.sterne_quiz += 1
                add_xp(2)
                users[st.session_state.user]["sterne"] = st.session_state.sterne
                save_json(USERS_FILE, users)
            else:
                st.error(f"Falsch! Richtige Antwort: {loesung}")
    with col2:
        if st.button("Nächste", key=f"next_{st.session_state.index}"):
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
    # auch Sterne speichern
    users[st.session_state.user]["sterne"] = st.session_state.sterne
    save_json(USERS_FILE, users)

# ================= FORTSCHRITT =================
st.subheader("📈 Lernfortschritt")
if st.session_state.user in progress:
    data = progress[st.session_state.user]
    df = pd.DataFrame(list(data.items()), columns=["Datum", "Sterne"])
    col_chart, col_space = st.columns([1,2])
    with col_chart:
        st.line_chart(df.set_index("Datum"))
