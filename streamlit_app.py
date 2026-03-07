
```python
import streamlit as st
import random
import json
import os
import pandas as pd
import datetime
import matplotlib.pyplot as plt

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
    "spiel_freigeschaltet": False,
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
                st.rerun()
            else:
                st.error("Falsche Daten")

    with col2:
        st.subheader("Registrieren")

        new_user = st.text_input("Neuer Benutzername")
        new_pw = st.text_input("Neues Passwort", type="password")

        if st.button("Account erstellen"):
            if new_user not in users:
                users[new_user] = {"password": new_pw, "sterne": 0, "klasse": 3}
                save_json(USERS_FILE, users)
                st.success("Account erstellt")
            else:
                st.error("Benutzer existiert bereits")

    st.stop()


# ================= HEADER =================

st.title("📚 Lern-App")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("⭐ Sterne", st.session_state.sterne)

with col2:
    klasse = st.slider("🎓 Klassenstufe", 1, 10, st.session_state.klasse)
    st.session_state.klasse = klasse

with col3:
    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()


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


# ================= FÄCHER =================

st.subheader("⚙️ Einstellungen")

col1, col2, col3 = st.columns(3)

with col1:
    fach = st.selectbox("Fach", ["Mathe", "Deutsch", "Englisch"])

with col2:
    thema = st.selectbox(
        "Thema",
        {
            "Mathe": ["Addition", "Subtraktion", "Multiplikation"],
            "Deutsch": ["Rechtschreibung"],
            "Englisch": ["Vokabeln"],
        }[fach],
    )

with col3:
    anzahl = st.slider("Aufgaben", 1, 10, 5)


if st.button("🚀 Quiz starten"):

    if fach == "Mathe":
        st.session_state.aufgaben = mathe_aufgaben(
            thema, st.session_state.klasse, anzahl
        )

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
            if antwort == loesung:
                st.success("Richtig ⭐")
                st.session_state.sterne += 1
                st.session_state.sterne_quiz += 1

    with col2:
        if st.button("Nächste"):
            st.session_state.index += 1

            if st.session_state.index >= len(st.session_state.aufgaben):
                st.session_state.fertig = True


# ================= ENDE =================

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

    fig = plt.figure()
    plt.plot(df["Datum"], df["Sterne"], marker="o")
    plt.xticks(rotation=45)

    st.pyplot(fig)


# ================= MINISPIEL =================

st.subheader("🎮 Minispiel-Shop")

if not st.session_state.spiel_freigeschaltet:

    st.write("Preis: ⭐ 10 Sterne")

    if st.button("Spiel kaufen"):

        if st.session_state.sterne >= 10:
            st.session_state.sterne -= 10
            st.session_state.spiel_freigeschaltet = True
        else:
            st.error("Nicht genug Sterne")


if st.session_state.spiel_freigeschaltet:

    st.subheader("🎯 Zahlen raten")

    if "zahl" not in st.session_state:
        st.session_state.zahl = random.randint(1, 20)

    guess = st.number_input("Rate die Zahl 1-20", 1, 20)

    if st.button("Raten"):

        if guess == st.session_state.zahl:
            st.success("Richtig! +2 Sterne ⭐")
            st.session_state.sterne += 2
            st.session_state.zahl = random.randint(1, 20)

        elif guess < st.session_state.zahl:
            st.info("Zu klein")

        else:
            st.info("Zu groß")
```

