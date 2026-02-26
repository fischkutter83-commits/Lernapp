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
for key, default in {
    "user": None,
    "aufgaben": [],
    "index": 0,
    "fertig": False,
}.items():
    st.session_state.setdefault(key, default)

# -------------------- LOGIN --------------------
if st.session_state.user is None:
    st.subheader("🔐 Login / Registrierung")
    username = st.text_input("Benutzername")
    password = st.text_input("Passwort", type="password")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Einloggen"):
            if users.get(username, {}).get("password") == password:
                st.session_state.user = username
                st.success(f"Willkommen, {username} 👋")
                st.rerun()
            else:
                st.error("❌ Benutzername oder Passwort falsch")

    with col2:
        if st.button("Registrieren"):
            if username in users:
                st.error("❌ Benutzer existiert bereits")
            else:
                users[username] = {"password": password}
                save_json(USERS_FILE, users)
                st.success("✅ Account erstellt – bitte einloggen")

    st.stop()

# -------------------- MATHE --------------------
def generiere_mathe_aufgaben(klasse, anzahl):
    aufgaben = []
    ops = ["Plus","Minus","Mal","Geteilt","Bruch","Potenz"] if klasse > 6 else ["Plus","Minus","Mal","Geteilt"]

    while len(aufgaben) < anzahl:
        art = random.choice(ops)

        if art == "Plus":
            a, b = random.randint(1, 50), random.randint(1, 50)
            frage = f"{a} + {b}"
            loesung = str(a + b)
            erklaerung = f"{a} + {b} = {a + b}"

        elif art == "Minus":
            a, b = random.randint(20, 50), random.randint(1, 20)
            frage = f"{a} - {b}"
            loesung = str(a - b)
            erklaerung = f"{a} - {b} = {a - b}"

        elif art == "Mal":
            a, b = random.randint(2, 12), random.randint(2, 12)
            frage = f"{a} × {b}"
            loesung = str(a * b)
            erklaerung = f"{a} × {b} = {a * b}"

        elif art == "Geteilt":
            b = random.randint(2, 12)
            ergebnis = random.randint(2, 12)
            a = b * ergebnis
            frage = f"{a} ÷ {b}"
            loesung = str(ergebnis)
            erklaerung = f"{a} ÷ {b} = {ergebnis}"

        elif art == "Bruch":
            a, b, c, d = [random.randint(1, 9) for _ in range(4)]
            f1, f2 = fractions.Fraction(a, b), fractions.Fraction(c, d)
            frage = f"{a}/{b} + {c}/{d}"
            loesung = str(f1 + f2)
            erklaerung = f"{f1} + {f2} = {f1 + f2}"

        elif art == "Potenz":
            a, b = random.randint(2, 9), random.randint(2, 4)
            frage = f"{a}^{b}"
            loesung = str(a ** b)
            erklaerung = f"{a}^{b} = {a ** b}"

        if frage not in [f[0] for f in aufgaben]:
            aufgaben.append((frage, loesung, erklaerung))

    return aufgaben

# -------------------- DEUTSCH --------------------
def generiere_deutsch_aufgaben(klasse, anzahl):
    daten = {
        1: ("Plural", {"Hund": "Hunde","Katze": "Katzen","Auto": "Autos"}),
        3: ("Artikel", {"Apfel": "der","Blume": "die","Haus": "das"}),
        5: ("Wortart", {"laufen": "Verb","schön": "Adjektiv","Baum": "Nomen"}),
        7: ("Synonym", {"groß": "riesig","klein": "winzig","schnell": "flink"})
    }
    stufe = max(k for k in daten if klasse >= k)
    thema, woerter = daten[stufe]

    aufgaben = []
    while len(aufgaben) < anzahl:
        wort, loesung = random.choice(list(woerter.items()))
        frage = f"{thema}: {wort}"
        erklaerung = f"Richtig ist: {loesung}"
        if frage not in [f[0] for f in aufgaben]:
            aufgaben.append((frage, loesung, erklaerung))
    return aufgaben

# -------------------- ENGLISCH --------------------
def generiere_englisch_aufgaben(klasse, anzahl):
    # Angepasst an Klassenniveau
    if klasse <= 2:
        woerter = {"rot": "red","blau": "blue","grün": "green","Hund":"dog","Katze":"cat"}
    elif klasse <= 4:
        woerter = {"Apfel":"apple","Haus":"house","Ball":"ball","Buch":"book"}
    elif klasse <= 6:
        woerter = {"gehen":"go","sehen":"see","kommen":"come","spielen":"play","lesen":"read"}
    elif klasse <= 8:
        woerter = {"schnell":"fast","groß":"big","klein":"small","glücklich":"happy","traurig":"sad"}
    else:  # Klasse 9-10
        woerter = {
            "Ich gehe zur Schule":"I go to school",
            "Er spielt Fußball":"He plays soccer",
            "Sie liest ein Buch":"She reads a book",
            "Wir essen Abendessen":"We eat dinner"
        }

    aufgaben = []
    while len(aufgaben) < anzahl:
        de, en = random.choice(list(woerter.items()))
        frage = f"Übersetze: {de}"
        erklaerung = f"{de} = {en}"
        if frage not in [f[0] for f in aufgaben]:
            aufgaben.append((frage, en, erklaerung))
    return aufgaben

# -------------------- Menü --------------------
st.sidebar.write(f"👤 Eingeloggt als: {st.session_state.user}")

fach = st.sidebar.radio("Fach:", ["Mathe", "Deutsch", "Englisch"])
klasse = st.sidebar.slider("Klassenstufe:", 1, 10, 1)
anzahl = st.sidebar.slider("Anzahl Aufgaben:", 1, 10, 5)

if st.sidebar.button("🧩 Quiz starten"):
    if fach == "Mathe":
        st.session_state.aufgaben = generiere_mathe_aufgaben(klasse, anzahl)
    elif fach == "Deutsch":
        st.session_state.aufgaben = generiere_deutsch_aufgaben(klasse, anzahl)
    else:
        st.session_state.aufgaben = generiere_englisch_aufgaben(klasse, anzahl)

    st.session_state.index = 0
    st.session_state.fertig = False
    st.rerun()

# -------------------- Quiz Ablauf --------------------
if st.session_state.aufgaben and not st.session_state.fertig:
    frage, loesung, erklaerung = st.session_state.aufgaben[st.session_state.index]

    st.subheader(f"Aufgabe {st.session_state.index + 1}")
    st.write(frage)

    antwort = st.text_input("Deine Antwort:")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Antwort prüfen"):
            if antwort.strip().lower() == loesung.strip().lower():
                st.success("✅ Richtig!")
            else:
                st.error("❌ Falsch!")
                st.info(erklaerung)

            progress.setdefault(st.session_state.user, []).append({
                "fach": fach,
                "frage": frage,
                "deine_antwort": antwort,
                "lösung": loesung
            })
            save_json(PROGRESS_FILE, progress)

    with col2:
        if st.button("Nächste Aufgabe"):
            st.session_state.index += 1
            if st.session_state.index >= len(st.session_state.aufgaben):
                st.session_state.fertig = True
            st.rerun()

elif st.session_state.fertig:
    st.success("🎉 Quiz beendet!")
    if st.button("🔁 Nochmal spielen"):
        st.session_state.aufgaben = []
        st.session_state.index = 0
        st.session_state.fertig = False
        st.rerun()

# -------------------- Fortschritt anzeigen (robust) --------------------
st.sidebar.subheader("Erledigt ✅")

if st.sidebar.button("Fortschritt anzeigen"):
    user_progress = progress.get(st.session_state.user, [])

    if not user_progress:
        st.info("Noch keine erledigten Aufgaben.")
    else:
        for e in user_progress:
            frage = e.get("frage", e.get("aufgabe", "❓ Unbekannt"))
            antwort = e.get("deine_antwort", e.get("antwort", "—"))
            loesung = e.get("lösung", e.get("loesung", "—"))
            fach = e.get("fach", "—")

            st.write(f"📘 **{fach}**: {frage} → {antwort} (Lösung: {loesung})")
            
