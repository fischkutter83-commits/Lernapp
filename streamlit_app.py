import streamlit as st
import random
import fractions
import json
import os

# -------------------- Seiten-Setup --------------------
st.set_page_config(page_title="Lern-App", layout="centered")
st.markdown("## 🎈 Lern-App für Kinder")
st.markdown("Lerne spielerisch Mathe, Deutsch und Englisch 📚✨")

USERS_FILE = "users.json"

# -------------------- User-Datei --------------------
def load_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

users = load_users()

# -------------------- Session State --------------------
defaults = {
    "user": None,
    "index": 0,
    "punkte": 0,
    "aufgaben": [],
    "fertig": False,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# -------------------- LOGIN --------------------
if st.session_state.user is None:
    st.subheader("🔐 Login / Registrierung")

    username = st.text_input("👤 Benutzername")
    password = st.text_input("🔑 Passwort", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Einloggen"):
            if username in users and users[username]["password"] == password:
                st.session_state.user = username
                st.success(f"Willkommen {username} 🎉")
                st.rerun()
            else:
                st.error("❌ Falsche Daten")

    with col2:
        if st.button("Registrieren"):
            if username in users:
                st.error("❌ Benutzer existiert schon")
            else:
                users[username] = {
                    "password": password,
                    "history": []
                }
                save_users(users)
                st.success("✅ Account erstellt")

    st.stop()

# -------------------- Aufgaben Generatoren --------------------
def generiere_mathe_aufgaben(klasse, anzahl):
    aufgaben = []
    ops = ["Plus", "Minus", "Mal", "Geteilt"]
    for _ in range(anzahl):
        art = random.choice(ops)
        if art == "Plus":
            a,b=random.randint(1,50),random.randint(1,50)
            aufgaben.append((f"{a} + {b}", a+b, f"{a}+{b}={a+b}"))
        elif art == "Minus":
            a,b=random.randint(20,50),random.randint(1,20)
            aufgaben.append((f"{a} - {b}", a-b, f"{a}-{b}={a-b}"))
        elif art == "Mal":
            a,b=random.randint(2,12),random.randint(2,12)
            aufgaben.append((f"{a} × {b}", a*b, f"{a}×{b}={a*b}"))
        else:
            b=random.randint(2,12)
            er=random.randint(2,12)
            aufgaben.append((f"{b*er} ÷ {b}", er, f"{b*er}÷{b}={er}"))
    return aufgaben

def generiere_deutsch_aufgaben(klasse, anzahl):
    daten={"Hund":"Hunde","Katze":"Katzen","gehen":"Verb","Haus":"Nomen"}
    aufgaben=[]
    for _ in range(anzahl):
        wort,loes=random.choice(list(daten.items()))
        aufgaben.append((f"Deutsch: {wort}", loes, f"Richtig: {loes}"))
    return aufgaben

def generiere_englisch_aufgaben(klasse, anzahl):
    daten={"Hund":"dog","Katze":"cat","rot":"red","blau":"blue"}
    aufgaben=[]
    for _ in range(anzahl):
        de,en=random.choice(list(daten.items()))
        aufgaben.append((f"Übersetze: {de}", en, f"{de} = {en}"))
    return aufgaben

# -------------------- Sidebar --------------------
st.sidebar.markdown(f"👤 **{st.session_state.user}**")

fach = st.sidebar.radio("📘 Fach", ["Mathe", "Deutsch", "Englisch"])
klasse = st.sidebar.slider("🎓 Klasse", 1, 10, 1)
anzahl = st.sidebar.slider("🧩 Aufgaben", 1, 10, 5)

if st.sidebar.button("🚀 Quiz starten"):
    if fach=="Mathe":
        st.session_state.aufgaben = generiere_mathe_aufgaben(klasse, anzahl)
    elif fach=="Deutsch":
        st.session_state.aufgaben = generiere_deutsch_aufgaben(klasse, anzahl)
    else:
        st.session_state.aufgaben = generiere_englisch_aufgaben(klasse, anzahl)

    st.session_state.index=0
    st.session_state.punkte=0
    st.session_state.fertig=False
    st.rerun()

# -------------------- Quiz --------------------
if st.session_state.aufgaben and not st.session_state.fertig:
    if st.session_state.index < len(st.session_state.aufgaben):
        frage, lösung, erklärung = st.session_state.aufgaben[st.session_state.index]

        st.markdown(f"### ✏️ Aufgabe {st.session_state.index+1}")
        st.info(frage)

        antwort = st.text_input("Deine Antwort", key=f"a{st.session_state.index}")

        col1,col2=st.columns(2)
        with col1:
            if st.button("✅ Prüfen"):
                if antwort.strip().lower()==str(lösung).strip().lower():
                    st.success("🎉 Richtig!")
                    st.session_state.punkte+=1
                else:
                    st.error("❌ Falsch")
                    st.info(erklärung)
                st.session_state.index+=1
                st.rerun()

        with col2:
            if st.button("🛑 Abbrechen"):
                st.session_state.fertig=True
                st.rerun()
    else:
        st.session_state.fertig=True
        st.rerun()

elif st.session_state.fertig and st.session_state.aufgaben:
    st.success(f"🏁 Fertig! Punkte: {st.session_state.punkte}/{len(st.session_state.aufgaben)}")
    if st.button("🔁 Neues Quiz"):
        st.session_state.aufgaben=[]
        st.session_state.index=0
        st.session_state.punkte=0
        st.session_state.fertig=False
        st.rerun()
