import streamlit as st
import random
import json
import os

st.set_page_config(page_title="Lern-App", layout="wide")
st.title("📚 Lern-App")

USERS_FILE = "users.json"


# ================= JSON =================

def load_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)

    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_users(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=4)


users = load_users()


# ================= SESSION STATE =================

defaults = {
    "user": None,
    "aufgaben": [],
    "index": 0,
    "fertig": False,
    "sterne": 0,
    "sterne_quiz": 0
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ================= LOGIN =================

if st.session_state.user is None:

    st.subheader("🔐 Login")

    username = st.text_input("Benutzername")
    password = st.text_input("Passwort", type="password")

    if st.button("Einloggen"):

        if username in users and users[username]["password"] == password:
            st.session_state.user = username
            st.session_state.sterne = users[username].get("sterne", 0)
            st.rerun()

        else:
            st.error("Falsche Zugangsdaten")

    st.divider()

    st.subheader("Registrieren")

    new_user = st.text_input("Neuer Benutzername")
    new_pw = st.text_input("Neues Passwort", type="password")

    if st.button("Account erstellen"):

        if new_user in users:
            st.error("Benutzer existiert bereits")
        else:
            users[new_user] = {"password": new_pw, "sterne": 0}
            save_users(users)
            st.success("Account erstellt!")

    st.stop()


# ================= AUFGABEN =================

def mathe_aufgaben(thema, klasse, anzahl):

    tasks = []

    for _ in range(anzahl):

        if thema == "Addition":
            a = random.randint(1, 100)
            b = random.randint(1, 100)
            tasks.append((f"{a} + {b}", str(a + b)))

        elif thema == "Subtraktion":
            a = random.randint(20, 100)
            b = random.randint(1, 20)
            tasks.append((f"{a} - {b}", str(a - b)))

        elif thema == "Multiplikation":
            a = random.randint(2, 12)
            b = random.randint(2, 12)
            tasks.append((f"{a} × {b}", str(a * b)))

        elif thema == "Division":
            b = random.randint(2, 10)
            r = random.randint(2, 10)
            tasks.append((f"{b*r} ÷ {b}", str(r)))

    return tasks


def deutsch_aufgaben(thema, anzahl):

    daten = {
        "Rechtschreibung": {
            "Hant": "Hand",
            "Fahrrat": "Fahrrad",
            "Interresse": "Interesse",
            "wierklich": "wirklich"
        },
        "Artikel": {
            "___ Hund": "der",
            "___ Katze": "die",
            "___ Auto": "das"
        }
    }

    pool = list(daten[thema].items())
    random.shuffle(pool)

    return pool[:anzahl]


def englisch_aufgaben(anzahl):

    vokabeln = {
        "Hund": "dog",
        "Katze": "cat",
        "Apfel": "apple",
        "denken": "think"
    }

    pool = list(vokabeln.items())
    random.shuffle(pool)

    return pool[:anzahl]


# ================= SIDEBAR =================

st.sidebar.write(f"👤 {st.session_state.user}")
st.sidebar.write(f"⭐ Sterne: {st.session_state.sterne}")

fach = st.sidebar.selectbox(
    "Fach",
    ["Mathe", "Deutsch", "Englisch"]
)

thema = st.sidebar.selectbox(
    "Thema",
    {
        "Mathe": ["Addition", "Subtraktion", "Multiplikation", "Division"],
        "Deutsch": ["Rechtschreibung", "Artikel"],
        "Englisch": ["Vokabeln"]
    }[fach]
)

anzahl = st.sidebar.slider("Aufgaben", 1, 10, 5)


if st.sidebar.button("🚀 Quiz starten"):

    if fach == "Mathe":
        st.session_state.aufgaben = mathe_aufgaben(thema, 3, anzahl)

    elif fach == "Deutsch":
        st.session_state.aufgaben = deutsch_aufgaben(thema, anzahl)

    else:
        st.session_state.aufgaben = englisch_aufgaben(anzahl)

    st.session_state.index = 0
    st.session_state.fertig = False
    st.session_state.sterne_quiz = 0

    st.rerun()


# ================= QUIZ =================

if st.session_state.aufgaben and not st.session_state.fertig:

    frage, loesung = st.session_state.aufgaben[st.session_state.index]

    st.subheader(f"Aufgabe {st.session_state.index + 1}")
    st.write(f"### {frage}")

    antwort = st.text_input("Deine Antwort")

    if st.button("Antwort prüfen"):

        if antwort.strip().lower() == loesung.lower():

            st.success("Richtig!")

            st.session_state.sterne_quiz += 1
            st.session_state.sterne += 1

            users[st.session_state.user]["sterne"] = st.session_state.sterne
            save_users(users)

        else:
            st.error(f"Falsch! Richtige Antwort: {loesung}")

    if st.button("Nächste Aufgabe"):

        st.session_state.index += 1

        if st.session_state.index >= len(st.session_state.aufgaben):
            st.session_state.fertig = True

        st.rerun()


# ================= ENDE =================

elif st.session_state.fertig:

    st.success(
        f"Quiz beendet! ⭐ {st.session_state.sterne_quiz} Sterne"
    )

    if st.button("Neues Quiz"):
        st.session_state.aufgaben = []
        st.session_state.fertig = False
        st.rerun()
