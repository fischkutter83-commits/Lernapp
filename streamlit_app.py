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
    "antwort": ""
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
def generiere_mathe_aufgaben(klasse, anzahl, themen):
    aufgaben = []
    ops = []
    if "Addition" in themen: ops.append("Plus")
    if "Subtraktion" in themen: ops.append("Minus")
    if "Multiplikation" in themen: ops.append("Mal")
    if "Division" in themen: ops.append("Geteilt")
    if "Brüche" in themen and klasse > 6: ops.append("Bruch")
    if "Potenzen" in themen and klasse > 6: ops.append("Potenz")

    while len(aufgaben) < anzahl:
        art = random.choice(ops)
        if art == "Plus":
            a, b = random.randint(1, 50), random.randint(1, 50)
            frage, loesung, erklaerung = f"{a} + {b}", str(a+b), f"{a} + {b} = {a+b}"
        elif art == "Minus":
            a, b = random.randint(20,50), random.randint(1,20)
            frage, loesung, erklaerung = f"{a} - {b}", str(a-b), f"{a} - {b} = {a-b}"
        elif art == "Mal":
            a, b = random.randint(2,12), random.randint(2,12)
            frage, loesung, erklaerung = f"{a} × {b}", str(a*b), f"{a} × {b} = {a*b}"
        elif art == "Geteilt":
            b = random.randint(2,12)
            ergebnis = random.randint(2,12)
            a = b * ergebnis
            frage, loesung, erklaerung = f"{a} ÷ {b}", str(ergebnis), f"{a} ÷ {b} = {ergebnis}"
        elif art == "Bruch":
            a,b,c,d = [random.randint(1,9) for _ in range(4)]
            f1,f2 = fractions.Fraction(a,b), fractions.Fraction(c,d)
            frage, loesung, erklaerung = f"{a}/{b} + {c}/{d}", str(f1+f2), f"{f1} + {f2} = {f1+f2}"
        elif art == "Potenz":
            a,b = random.randint(2,9), random.randint(2,4)
            frage, loesung, erklaerung = f"{a}^{b}", str(a**b), f"{a}^{b} = {a**b}"
        if frage not in [f[0] for f in aufgaben]:
            aufgaben.append((frage, loesung, erklaerung))
    return aufgaben

# -------------------- DEUTSCH --------------------
def generiere_deutsch_aufgaben(klasse, anzahl, themen):
    daten = {
        1: {"Plural": {"Hund":"Hunde","Katze":"Katzen","Auto":"Autos"},
            "Artikel": {"Apfel":"der","Blume":"die","Haus":"das"},
            "Wortart": {"laufen":"Verb","schön":"Adjektiv","Baum":"Nomen"}},
        5: {"Synonym": {"groß":"riesig","klein":"winzig","schnell":"flink"},
            "Plural": {"Maus":"Mäuse","Blume":"Blumen","Auto":"Autos"},
            "Artikel": {"Buch":"das","Stuhl":"der","Tisch":"der"}}
    }
    stufe = max(k for k in daten if klasse >= k)
    alle_themen = {k:v for k,v in daten[stufe].items() if k in themen}
    alle_aufgaben = []
    while len(alle_aufgaben) < anzahl:
        thema, woerter = random.choice(list(alle_themen.items()))
        wort, loesung = random.choice(list(woerter.items()))
        frage, erklaerung = f"{thema}: {wort}", f"Richtig ist: {loesung}"
        if frage not in [f[0] for f in alle_aufgaben]:
            alle_aufgaben.append((frage, loesung, erklaerung))
    return alle_aufgaben

# -------------------- ENGLISCH --------------------
def generiere_englisch_aufgaben(klasse, anzahl, themen):
    themen_dict = {}
    if "Farben" in themen: themen_dict.update({"rot":"red","blau":"blue","grün":"green"})
    if "Tiere" in themen: themen_dict.update({"Hund":"dog","Katze":"cat","Haus":"house"})
    if "Verben" in themen and klasse>=5: themen_dict.update({"gehen":"go","sehen":"see","kommen":"come"})
    if "Adjektive" in themen and klasse>=7: themen_dict.update({"schnell":"fast","groß":"big","klein":"small","glücklich":"happy"})
    if "Sätze" in themen and klasse>=9: themen_dict.update({
        "Ich gehe zur Schule":"I go to school",
        "Er spielt Fußball":"He plays soccer",
        "Sie liest ein Buch":"She reads a book",
        "Wir essen Abendessen":"We eat dinner"
    })
    aufgaben = []
    while len(aufgaben) < anzahl:
        de, en = random.choice(list(themen_dict.items()))
        frage, erklaerung = f"Übersetze: {de}", f"{de} = {en}"
        if frage not in [f[0] for f in aufgaben]:
            aufgaben.append((frage, en, erklaerung))
    return aufgaben

# -------------------- Sidebar Menü --------------------
st.sidebar.write(f"👤 Eingeloggt als: {st.session_state.user}")
fach = st.sidebar.radio("Fach:", ["Mathe", "Deutsch", "Englisch"])
klasse = st.sidebar.slider("Klassenstufe:", 1, 10, 1)
anzahl = st.sidebar.slider("Anzahl Aufgaben:", 1, 10, 5)

# Unterthemen
if fach=="Mathe":
    unterthemen = st.sidebar.multiselect("Unterthemen Mathe:", ["Addition","Subtraktion","Multiplikation","Division","Brüche","Potenzen"], default=["Addition"])
elif fach=="Deutsch":
    unterthemen = st.sidebar.multiselect("Unterthemen Deutsch:", ["Plural","Artikel","Wortart","Synonym"], default=["Plural"])
else:
    unterthemen = st.sidebar.multiselect("Unterthemen Englisch:", ["Farben","Tiere","Verben","Adjektive","Sätze"], default=["Farben"])

if st.sidebar.button("🧩 Quiz starten"):
    if fach=="Mathe": st.session_state.aufgaben = generiere_mathe_aufgaben(klasse, anzahl, unterthemen)
    elif fach=="Deutsch": st.session_state.aufgaben = generiere_deutsch_aufgaben(klasse, anzahl, unterthemen)
    else: st.session_state.aufgaben = generiere_englisch_aufgaben(klasse, anzahl, unterthemen)
    st.session_state.index = 0
    st.session_state.fertig = False
    st.rerun()

# -------------------- Quiz Ablauf --------------------
if st.session_state.aufgaben and not st.session_state.fertig:
    frage, loesung, erklaerung = st.session_state.aufgaben[st.session_state.index]
    st.subheader(f"Aufgabe {st.session_state.index+1}")
    st.write(frage)

    # Antwortfeld mit Enter-Taste
    st.session_state.antwort = st.text_input("Deine Antwort:", value=st.session_state.antwort, key="antwort_input", on_change=lambda: st.session_state.button_pruefen=True)
    
    # Prüfen
    if st.session_state.get("button_pruefen", False):
        if st.session_state.antwort.strip().lower() == loesung.strip().lower():
            st.success("✅ Richtig!")
        else:
            st.error("❌ Falsch!")
            st.info(erklaerung)

        progress.setdefault(st.session_state.user, []).append({
            "fach": fach,
            "frage": frage,
            "deine_antwort": st.session_state.antwort,
            "lösung": loesung
        })
        save_json(PROGRESS_FILE, progress)

        st.session_state.antwort = ""
        st.session_state.index += 1
        st.session_state.button_pruefen = False
        if st.session_state.index >= len(st.session_state.aufgaben):
            st.session_state.fertig = True
        st.experimental_rerun()

elif st.session_state.fertig:
    st.success("🎉 Quiz beendet!")
    if st.button("🔁 Nochmal spielen"):
        st.session_state.aufgaben = []
        st.session_state.index = 0
        st.session_state.fertig = False
        st.rerun()

# -------------------- Fortschritt --------------------
st.sidebar.subheader("Erledigt ✅")
if st.sidebar.button("Fortschritt anzeigen"):
    user_progress = progress.get(st.session_state.user, [])
    if not user_progress:
        st.info("Noch keine erledigten Aufgaben.")
    else:
        for e in user_progress:
            frage = e.get("frage","❓ Unbekannt")
            antwort = e.get("deine_antwort","—")
            loesung = e.get("lösung","—")
            fach = e.get("fach","—")
            st.write(f"📘 **{fach}**: {frage} → {antwort} (Lösung: {loesung})")
