import streamlit as st
import random
import fractions
import json
import os

# -------------------- Grundeinstellungen --------------------
st.set_page_config(page_title="Lern-App", layout="centered")
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
if "user" not in st.session_state:
    st.session_state.user = None
if "aufgaben" not in st.session_state:
    st.session_state.aufgaben = []
if "index" not in st.session_state:
    st.session_state.index = 0
if "fertig" not in st.session_state:
    st.session_state.fertig = False
if "antwort" not in st.session_state:
    st.session_state.antwort = ""
for key, default in {
    "user": None,
    "aufgaben": [],
    "index": 0,
    "fertig": False,
}.items():
    st.session_state.setdefault(key, default)

# -------------------- LOGIN --------------------
if st.session_state.user is None:
@@ -50,13 +47,13 @@
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Einloggen"):
            user_data = users.get(username)
            if isinstance(user_data, dict) and user_data.get("password") == password:
            if users.get(username, {}).get("password") == password:
                st.session_state.user = username
                st.success(f"Willkommen, {username} 👋")
                st.rerun()
            else:
                st.error("❌ Benutzername oder Passwort falsch")

    with col2:
        if st.button("Registrieren"):
            if username in users:
@@ -65,65 +62,108 @@
                users[username] = {"password": password}
                save_json(USERS_FILE, users)
                st.success("✅ Account erstellt – bitte einloggen")

    st.stop()

# -------------------- Aufgabengeneratoren --------------------
# -------------------- MATHE --------------------
def generiere_mathe_aufgaben(klasse, anzahl):
    aufgaben = []
    ops = ["Plus","Minus","Mal","Geteilt","Bruch","Potenz"] if klasse > 6 else ["Plus","Minus","Mal","Geteilt"]

    for _ in range(anzahl):
        art = random.choice(ops)

        if art == "Plus":
            a, b = random.randint(1, 50), random.randint(1, 50)
            aufgaben.append((f"{a} + {b}", str(a + b), f"{a} + {b} = {a + b}"))

        elif art == "Minus":
            a, b = random.randint(20, 50), random.randint(1, 20)
            aufgaben.append((f"{a} - {b}", str(a - b), f"{a} - {b} = {a - b}"))

        elif art == "Mal":
            a, b = random.randint(2, 12), random.randint(2, 12)
            aufgaben.append((f"{a} × {b}", str(a * b), f"{a} × {b} = {a * b}"))

        elif art == "Geteilt":
            b = random.randint(2, 12)
            ergebnis = random.randint(2, 12)
            a = b * ergebnis
            aufgaben.append((f"{a} ÷ {b}", str(ergebnis), f"{a} ÷ {b} = {ergebnis}"))

        elif art == "Bruch":
            a, b, c, d = [random.randint(1, 9) for _ in range(4)]
            f1, f2 = fractions.Fraction(a, b), fractions.Fraction(c, d)
            aufgaben.append((f"{a}/{b} + {c}/{d}", str(f1 + f2), f"{a}/{b} + {c}/{d} = {f1 + f2}"))
            aufgaben.append((f"{a}/{b} + {c}/{d}", str(f1 + f2), f"{f1} + {f2} = {f1 + f2}"))

        elif art == "Potenz":
            a, b = random.randint(2, 9), random.randint(2, 4)
            aufgaben.append((f"{a}^{b}", str(a ** b), f"{a}^{b} = {a ** b}"))

    return aufgaben

# -------------------- DEUTSCH --------------------
def generiere_deutsch_aufgaben(klasse, anzahl):
    themen = {
        1: ("Plural", {"Hund": "Hunde", "Katze": "Katzen"}),
        4: ("Wortart", {"laufen": "Verb", "Haus": "Nomen"}),
        7: ("Synonym", {"groß": "riesig", "klein": "winzig"})
    daten = {
        1: ("Plural", {
            "Hund": "Hunde",
            "Katze": "Katzen",
            "Auto": "Autos"
        }),
        3: ("Artikel", {
            "Apfel": "der",
            "Blume": "die",
            "Haus": "das"
        }),
        5: ("Wortart", {
            "laufen": "Verb",
            "schön": "Adjektiv",
            "Baum": "Nomen"
        }),
        7: ("Synonym", {
            "groß": "riesig",
            "klein": "winzig",
            "schnell": "flink"
        })
    }
    thema, woerter = themen[max(k for k in themen if klasse >= k)]

    stufe = max(k for k in daten if klasse >= k)
    thema, woerter = daten[stufe]

    aufgaben = []
    for _ in range(anzahl):
        wort, loesung = random.choice(list(woerter.items()))
        aufgaben.append((f"{thema}: {wort}", loesung, f"Richtig: {loesung}"))
        aufgaben.append(
            (f"{thema}: {wort}", loesung, f"Richtig ist: {loesung}")
        )

    return aufgaben

# -------------------- ENGLISCH --------------------
def generiere_englisch_aufgaben(klasse, anzahl):
    daten = (
        {"rot": "red", "blau": "blue"} if klasse <= 2
        else {"Hund": "dog", "Katze": "cat"} if klasse <= 4
        else {"gehen": "go", "sehen": "see"}
    )
    daten = {
        1: {"rot": "red", "blau": "blue", "grün": "green"},
        3: {"Hund": "dog", "Katze": "cat", "Haus": "house"},
        5: {"gehen": "go", "sehen": "see", "kommen": "come"},
        7: {"schnell": "fast", "groß": "big", "klein": "small"}
    }

    stufe = max(k for k in daten if klasse >= k)
    woerter = daten[stufe]

    aufgaben = []
    for _ in range(anzahl):
        de, en = random.choice(list(daten.items()))
        aufgaben.append((f"Übersetze: {de}", en, f"{de} = {en}"))
        de, en = random.choice(list(woerter.items()))
        aufgaben.append(
            (f"Übersetze: {de}", en, f"{de} = {en}")
        )

    return aufgaben

# -------------------- Menü --------------------
st.sidebar.write(f"👤 Eingeloggt als: {st.session_state.user}")
fach = st.sidebar.radio("Fach wählen:", ["Mathe", "Deutsch", "Englisch"])

fach = st.sidebar.radio("Fach:", ["Mathe", "Deutsch", "Englisch"])
klasse = st.sidebar.slider("Klassenstufe:", 1, 10, 1)
anzahl = st.sidebar.slider("Anzahl Aufgaben:", 1, 10, 5)

@@ -137,21 +177,19 @@

    st.session_state.index = 0
    st.session_state.fertig = False
    st.session_state.antwort = ""
    st.rerun()

# -------------------- Quiz Ablauf --------------------
if st.session_state.aufgaben and not st.session_state.fertig:
    frage, loesung, erklaerung = st.session_state.aufgaben[st.session_state.index]

    st.subheader(f"Aufgabe {st.session_state.index + 1}")
    st.write(frage)

    antwort = st.text_input(
        "Deine Antwort:",
        key=f"antwort_{st.session_state.index}"
    )
    antwort = st.text_input("Deine Antwort:")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Antwort prüfen"):
            if antwort.strip().lower() == loesung.strip().lower():
@@ -181,15 +219,21 @@
        st.session_state.aufgaben = []
        st.session_state.index = 0
        st.session_state.fertig = False
        st.session_state.antwort = ""
        st.rerun()

# -------------------- Fortschritt anzeigen --------------------
# -------------------- Fortschritt anzeigen (robust) --------------------
st.sidebar.subheader("Erledigt ✅")

if st.sidebar.button("Fortschritt anzeigen"):
    user_progress = progress.get(st.session_state.user, [])
    if user_progress:
        for e in user_progress:
            st.write(f"{e['frage']} → {e['deine_antwort']} (Lösung: {e['lösung']})")
    else:

    if not user_progress:
        st.info("Noch keine erledigten Aufgaben.")
    else:
        for e in user_progress:
            frage = e.get("frage", e.get("aufgabe", "❓ Unbekannt"))
            antwort = e.get("deine_antwort", e.get("antwort", "—"))
            loesung = e.get("lösung", e.get("loesung", "—"))
            fach = e.get("fach", "—")

            st.write(f"📘 **{fach}**: {frage} → {antwort} (Lösung: {loesung})")
