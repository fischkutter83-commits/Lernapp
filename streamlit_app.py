import streamlit as st
import random
import fractions
import json
import os

# -------------------- Grundeinstellungen --------------------
st.set_page_config(page_title="Lern-App", layout="centered")
st.title("📚 Lern-App")

USERS_FILE = "users.json"

# -------------------- User-Datei laden / speichern --------------------
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
if "user" not in st.session_state:
    st.session_state.user = None
if "index" not in st.session_state:
    st.session_state.index = 0
if "punkte" not in st.session_state:
    st.session_state.punkte = 0
if "aufgaben" not in st.session_state:
    st.session_state.aufgaben = []
if "fertig" not in st.session_state:
    st.session_state.fertig = False

# -------------------- LOGIN --------------------
if st.session_state.user is None:
    st.subheader("🔐 Login / Registrierung")

    username = st.text_input("Benutzername")
    password = st.text_input("Passwort", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Einloggen"):
            if username in users and users[username]["password"] == password:
                st.session_state.user = username
                st.success(f"Willkommen, {username} 👋")
                st.experimental_rerun()
            else:
                st.error("❌ Benutzername oder Passwort falsch")

    with col2:
        if st.button("Registrieren"):
            if username in users:
                st.error("❌ Benutzer existiert bereits")
            else:
                users[username] = {
                    "password": password
                }
                save_users(users)
                st.success("✅ Account erstellt – bitte einloggen")

    st.stop()

# -------------------- Mathe-Aufgaben --------------------
def generiere_mathe_aufgaben(klasse, anzahl):
    aufgaben = []
    if klasse <= 2:
        ops = ["Plus", "Minus"]
    elif klasse <= 6:
        ops = ["Plus", "Minus", "Mal", "Geteilt"]
    else:
        ops = ["Plus", "Minus", "Mal", "Geteilt", "Bruch", "Potenz"]

    for _ in range(anzahl):
        art = random.choice(ops)

        if art == "Plus":
            a, b = random.randint(1, 50), random.randint(1, 50)
            aufgaben.append((f"{a} + {b}", a + b, f"{a} + {b} = {a+b}"))

        elif art == "Minus":
            a, b = random.randint(20, 50), random.randint(1, 20)
            aufgaben.append((f"{a} - {b}", a - b, f"{a} - {b} = {a-b}"))

        elif art == "Mal":
            a, b = random.randint(2, 12), random.randint(2, 12)
            aufgaben.append((f"{a} × {b}", a * b, f"{a} × {b} = {a*b}"))

        elif art == "Geteilt":
            b = random.randint(2, 12)
            ergebnis = random.randint(2, 12)
            a = b * ergebnis
            aufgaben.append((f"{a} ÷ {b}", ergebnis, f"{a} ÷ {b} = {ergebnis}"))

        elif art == "Bruch":
            a, b = random.randint(1, 9), random.randint(1, 9)
            c, d = random.randint(1, 9), random.randint(1, 9)
            f1, f2 = fractions.Fraction(a, b), fractions.Fraction(c, d)
            aufgaben.append(
                (f"{a}/{b} + {c}/{d}", str(f1 + f2),
                 f"{a}/{b} + {c}/{d} = {f1 + f2}")
            )

        elif art == "Potenz":
            a, b = random.randint(2, 9), random.randint(2, 4)
            aufgaben.append((f"{a}^{b}", a**b, f"{a}^{b} = {a**b}"))

    return aufgaben

# -------------------- Deutsch --------------------
def generiere_deutsch_aufgaben(klasse, anzahl):
    daten = {
        1: ("Plural", {"Hund": "Hunde", "Katze": "Katzen"}),
        4: ("Wortart", {"laufen": "Verb", "Haus": "Nomen"}),
        7: ("Synonym", {"groß": "riesig", "klein": "winzig"})
    }
    thema, wörter = daten[max(k for k in daten if klasse >= k)]

    aufgaben = []
    for _ in range(anzahl):
        wort, lösung = random.choice(list(wörter.items()))
        aufgaben.append((f"{thema}: {wort}", lösung, f"Richtig: {lösung}"))
    return aufgaben

# -------------------- Englisch --------------------
def generiere_englisch_aufgaben(klasse, anzahl):
    if klasse <= 2:
        daten = {"rot": "red", "blau": "blue"}
    elif klasse <= 4:
        daten = {"Hund": "dog", "Katze": "cat"}
    else:
        daten = {"gehen": "go", "sehen": "see"}

    aufgaben = []
    for _ in range(anzahl):
        de, en = random.choice(list(daten.items()))
        aufgaben.append((f"Übersetze: {de}", en, f"{de} = {en}"))
    return aufgaben

# -------------------- Menü --------------------
st.sidebar.write(f"👤 Eingeloggt als: {st.session_state.user}")

fach = st.sidebar.radio("Fach", ["Mathe", "Deutsch", "Englisch"])
klasse = st.sidebar.slider("Klasse", 1, 10, 1)
anzahl = st.sidebar.slider("Aufgaben", 1, 10, 5)

if st.sidebar.button("🧩 Quiz starten"):
    if fach == "Mathe":
        st.session_state.aufgaben = generiere_mathe_aufgaben(klasse, anzahl)
    elif fach == "Deutsch":
        st.session_state.aufgaben = generiere_deutsch_aufgaben(klasse, anzahl)
    else:
        st.session_state.aufgaben = generiere_englisch_aufgaben(klasse, anzahl)

    st.session_state.index = 0
    st.session_state.punkte = 0
    st.session_state.fertig = False

# -------------------- Quiz --------------------
if st.session_state.aufgaben and not st.session_state.fertig:
    frage, lösung, erklärung = st.session_state.aufgaben[st.session_state.index]
    st.subheader(f"Aufgabe {st.session_state.index + 1}")
    st.write(frage)
    antwort = st.text_input("Deine Antwort")

    if st.button("Antwort prüfen"):
        if antwort.strip().lower() == str(lösung).strip().lower():
            st.success("✅ Richtig")
            st.session_state.punkte += 1
        else:
            st.error("❌ Falsch")
            st.info(erklärung)

        if st.session_state.index + 1 < len(st.session_state.aufgaben):
            st.session_state.index += 1
            st.experimental_rerun()
        else:
            st.session_state.fertig = True
            st.experimental_rerun()

elif st.session_state.fertig:
    st.success(f"🎉 Fertig! Punkte: {st.session_state.punkte}")
    if st.button("Nochmal"):
        st.session_state.aufgaben = []
