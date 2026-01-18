import streamlit as st
import random
import fractions
import json
import os

# -------------------- Grundeinstellungen --------------------
st.set_page_config(page_title="📚 Lern-App", layout="wide")
st.title("📚 Lern-App")

USERS_FILE = "users.json"
PROGRESS_FILE = "progress.json"

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

def load_progress():
    if not os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "w") as f:
            json.dump({}, f)
    with open(PROGRESS_FILE, "r") as f:
        return json.load(f)

def save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=4)

users = load_users()
progress = load_progress()

# -------------------- Session State --------------------
if "user" not in st.session_state:
    st.session_state.user = None
if "quiz_aktiv" not in st.session_state:
    st.session_state.quiz_aktiv = False
if "aufgaben" not in st.session_state:
    st.session_state.aufgaben = []
if "index" not in st.session_state:
    st.session_state.index = 0
if "punkte" not in st.session_state:
    st.session_state.punkte = 0
if "feedback" not in st.session_state:
    st.session_state.feedback = ""

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
                users[username] = {"password": password}
                save_users(users)
                st.success("✅ Account erstellt – bitte einloggen")

    st.stop()

# -------------------- Mathe-Aufgaben --------------------
def generiere_mathe_aufgaben(klasse, anzahl, thema=None):
    aufgaben = []
    operationen = ["Plus", "Minus", "Mal", "Geteilt", "Bruch", "Potenz"]
    if klasse <= 2:
        operationen = ["Plus", "Minus"]
    elif klasse <= 6:
        operationen = ["Plus", "Minus", "Mal", "Geteilt"]
    
    for _ in range(anzahl):
        art = thema if thema else random.choice(operationen)
        if art == "Plus":
            a, b = random.randint(1,50), random.randint(1,50)
            aufgaben.append((f"{a} + {b}", a+b, f"{a} + {b} = {a+b}"))
        elif art == "Minus":
            a,b = random.randint(20,50), random.randint(1,20)
            aufgaben.append((f"{a} - {b}", a-b, f"{a} - {b} = {a-b}"))
        elif art == "Mal":
            a,b = random.randint(2,12), random.randint(2,12)
            aufgaben.append((f"{a} × {b}", a*b, f"{a} × {b} = {a*b}"))
        elif art == "Geteilt":
            b = random.randint(2,12)
            ergebnis = random.randint(2,12)
            a = b * ergebnis
            aufgaben.append((f"{a} ÷ {b}", ergebnis, f"{a} ÷ {b} = {ergebnis}"))
        elif art == "Bruch":
            a,b = random.randint(1,9), random.randint(1,9)
            c,d = random.randint(1,9), random.randint(1,9)
            f1,f2 = fractions.Fraction(a,b), fractions.Fraction(c,d)
            aufgaben.append((f"{a}/{b} + {c}/{d}", str(f1+f2), f"{a}/{b} + {c}/{d} = {f1+f2}"))
        elif art == "Potenz":
            a,b = random.randint(2,9), random.randint(2,4)
            aufgaben.append((f"{a}^{b}", a**b, f"{a}^{b} = {a**b}"))
    return aufgaben

# -------------------- Deutsch --------------------
def generiere_deutsch_aufgaben(klasse, anzahl, thema=None):
    daten = {
        1: ("Plural", {"Hund":"Hunde","Katze":"Katzen"}),
        4: ("Wortart", {"laufen":"Verb","Haus":"Nomen"}),
        7: ("Synonym", {"groß":"riesig","klein":"winzig"})
    }
    t,wörter = daten[max(k for k in daten if klasse>=k)]
    if thema:
        t = thema

    aufgaben = []
    for _ in range(anzahl):
        wort, lösung = random.choice(list(wörter.items()))
        aufgaben.append((f"{t}: {wort}", lösung, f"Richtig: {lösung}"))
    return aufgaben

# -------------------- Englisch --------------------
def generiere_englisch_aufgaben(klasse, anzahl, thema=None):
    if klasse<=2: daten = {"rot":"red","blau":"blue"}
    elif klasse<=4: daten = {"Hund":"dog","Katze":"cat"}
    else: daten = {"gehen":"go","sehen":"see"}
    aufgaben = []
    for _ in range(anzahl):
        de,en = random.choice(list(daten.items()))
        aufgaben.append((f"Übersetze: {de}", en, f"{de} = {en}"))
    return aufgaben

# -------------------- Sidebar --------------------
st.sidebar.write(f"👤 Eingeloggt als: {st.session_state.user}")
fach = st.sidebar.radio("Fach", ["Mathe","Deutsch","Englisch"])
klasse = st.sidebar.slider("Klasse",1,10,1)
anzahl = st.sidebar.slider("Aufgaben",1,10,5)

st.sidebar.write("**Aufgabenart wählen:**")
aufgaben_art = st.sidebar.radio("Art", ["Zufall", "Thema"])

thema = None
if aufgaben_art == "Thema":
    thema = st.sidebar.text_input("Thema eingeben (z.B. Plus, Minus)")

# Start Quiz
if st.sidebar.button("🧩 Quiz starten"):
    if fach=="Mathe": st.session_state.aufgaben = generiere_mathe_aufgaben(klasse,anzahl,thema)
    elif fach=="Deutsch": st.session_state.aufgaben = generiere_deutsch_aufgaben(klasse,anzahl,thema)
    else: st.session_state.aufgaben = generiere_englisch_aufgaben(klasse,anzahl,thema)
    st.session_state.index = 0
    st.session_state.punkte = 0
    st.session_state.feedback = ""
    st.session_state.quiz_aktiv = True

# -------------------- Quiz Ablauf --------------------
if st.session_state.quiz_aktiv:
    if st.session_state.index < len(st.session_state.aufgaben):
        frage, lösung, erklärung = st.session_state.aufgaben[st.session_state.index]
        st.subheader(f"Aufgabe {st.session_state.index +1}")
        st.write(frage)

        antwort_key = f"antwort_{st.session_state.index}"
        if antwort_key not in st.session_state:
            st.session_state[antwort_key] = ""

        antwort = st.text_input("Antwort", key=antwort_key)

        if st.button("✔️ Abgeben"):
            if antwort.strip().lower() == str(lösung).strip().lower():
                st.session_state.punkte +=1
                st.session_state.feedback = "✅ Richtig!"
            else:
                st.session_state.feedback = f"❌ Falsch! {erklärung}"

            # Speichern für den User
            if st.session_state.user not in progress:
                progress[st.session_state.user] = []
            progress[st.session_state.user].append({
                "fach": fach,
                "aufgabe": frage,
                "antwort": antwort,
                "richtig": antwort.strip().lower()==str(lösung).strip().lower()
            })
            save_progress(progress)

            # Textfeld zurücksetzen + nächste Aufgabe
            st.session_state[antwort_key] = ""
            st.session_state.index +=1

        if st.session_state.feedback:
            st.info(st.session_state.feedback)

    else:
        st.success(f"🎉 Quiz beendet! Punkte: {st.session_state.punkte}/{len(st.session_state.aufgaben)}")
        if st.button("🔁 Nochmal"):
            st.session_state.quiz_aktiv = False

# -------------------- Fertige Aufgaben ansehen --------------------
st.sidebar.write("---")
st.sidebar.write("📂 Erledigte Aufgaben ansehen")
fach_show = st.sidebar.radio("Fach auswählen:", ["Mathe","Deutsch","Englisch"], key="fach_show")
if st.sidebar.button("📖 Anzeigen"):
    user_prog = progress.get(st.session_state.user,[])
    fach_prog = [p for p in user_prog if p["fach"]==fach_show]
    st.subheader(f"📂 {fach_show} Aufgaben")
    for i,p in enumerate(fach_prog):
        status = "✅ Richtig" if p["richtig"] else "❌ Falsch"
        st.write(f"{i+1}. {p['aufgabe']} → {status} (Deine Antwort: {p['antwort']})")
