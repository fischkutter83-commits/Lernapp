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

# -------------------- User-Datei laden / speichern --------------------
def load_json(file):
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump({}, f)
    with open(file, "r") as f:
        return json.load(f)

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
                save_json(USERS_FILE, users)
                st.success("✅ Account erstellt – bitte einloggen")
    st.stop()

# -------------------- Aufgabengeneratoren --------------------
def generiere_mathe_aufgaben(klasse, anzahl):
    aufgaben = []
    ops = ["Plus","Minus","Mal","Geteilt","Bruch","Potenz"] if klasse>6 else ["Plus","Minus","Mal","Geteilt"]
    for _ in range(anzahl):
        art = random.choice(ops)
        if art=="Plus":
            a,b=random.randint(1,50),random.randint(1,50)
            aufgaben.append((f"{a} + {b}", str(a+b), f"{a} + {b} = {a+b}"))
        elif art=="Minus":
            a,b=random.randint(20,50),random.randint(1,20)
            aufgaben.append((f"{a} - {b}", str(a-b), f"{a} - {b} = {a-b}"))
        elif art=="Mal":
            a,b=random.randint(2,12),random.randint(2,12)
            aufgaben.append((f"{a} × {b}", str(a*b), f"{a} × {b} = {a*b}"))
        elif art=="Geteilt":
            b=random.randint(2,12)
            ergebnis=random.randint(2,12)
            a=b*ergebnis
            aufgaben.append((f"{a} ÷ {b}", str(ergebnis), f"{a} ÷ {b} = {ergebnis}"))
        elif art=="Bruch":
            a,b,c,d=random.randint(1,9),random.randint(1,9),random.randint(1,9),random.randint(1,9)
            f1,f2=fractions.Fraction(a,b),fractions.Fraction(c,d)
            aufgaben.append((f"{a}/{b} + {c}/{d}", str(f1+f2), f"{a}/{b} + {c}/{d} = {f1+f2}"))
        elif art=="Potenz":
            a,b=random.randint(2,9),random.randint(2,4)
            aufgaben.append((f"{a}^{b}", str(a**b), f"{a}^{b} = {a**b}"))
    return aufgaben

def generiere_deutsch_aufgaben(klasse, anzahl):
    themen = {1:("Plural",{"Hund":"Hunde","Katze":"Katzen"}),
              4:("Wortart",{"laufen":"Verb","Haus":"Nomen"}),
              7:("Synonym",{"groß":"riesig","klein":"winzig"})}
    thema,wörter=themen[max(k for k in themen if klasse>=k)]
    aufgaben=[]
    for _ in range(anzahl):
        wort,loesung=random.choice(list(wörter.items()))
        aufgaben.append((f"{thema}: {wort}", loesung, f"Richtig: {loesung}"))
    return aufgaben

def generiere_englisch_aufgaben(klasse,anzahl):
    daten = {"rot":"red","blau":"blue"} if klasse<=2 else {"Hund":"dog","Katze":"cat"} if klasse<=4 else {"gehen":"go","sehen":"see"}
    aufgaben=[]
    for _ in range(anzahl):
        de,en=random.choice(list(daten.items()))
        aufgaben.append((f"Übersetze: {de}", en, f"{de} = {en}"))
    return aufgaben

# -------------------- Menü --------------------
st.sidebar.write(f"👤 Eingeloggt als: {st.session_state.user}")
fach = st.sidebar.radio("Fach wählen:", ["Mathe","Deutsch","Englisch"])
klasse = st.sidebar.slider("Klassenstufe:",1,10,1)
modus = st.sidebar.radio("Aufgabentyp:", ["Zufall","Thema"])
anzahl = st.sidebar.slider("Anzahl Aufgaben:",1,10,5)

if st.sidebar.button("🧩 Quiz starten"):
    if fach=="Mathe":
        st.session_state.aufgaben=generiere_mathe_aufgaben(klasse,anzahl)
    elif fach=="Deutsch":
        st.session_state.aufgaben=generiere_deutsch_aufgaben(klasse,anzahl)
    else:
        st.session_state.aufgaben=generiere_englisch_aufgaben(klasse,anzahl)
    st.session_state.index=0
    st.session_state.fertig=False
    st.session_state.antwort=""

# -------------------- Quiz Ablauf --------------------
if st.session_state.aufgaben and not st.session_state.fertig:
    frage, loesung, erklaerung = st.session_state.aufgaben[st.session_state.index]
    st.subheader(f"Aufgabe {st.session_state.index+1}")
    st.write(frage)
    st.session_state.antwort = st.text_input("Deine Antwort:", value="", key=f"antwort_{st.session_state.index}")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Antwort prüfen"):
            if st.session_state.antwort.strip().lower()==loesung.strip().lower():
                st.success("✅ Richtig!")
            else:
                st.error("❌ Falsch!")
                st.info(erklaerung)
            # Fortschritt speichern
            if st.session_state.user not in progress:
                progress[st.session_state.user]=[]
            progress[st.session_state.user].append({"fach":fach,"frage":frage,"antwort":st.session_state.antwort,"loesung":loesung})
            save_json(PROGRESS_FILE,progress)
    with col2:
        if st.button("Nächste Aufgabe"):
            st.session_state.index+=1
            st.session_state.antwort=""
            if st.session_state.index>=len(st.session_state.aufgaben):
                st.session_state.fertig=True
            st.experimental_rerun()

elif st.session_state.fertig:
    st.success(f"🎉 Quiz beendet!")
    if st.sidebar.button("🔁 Nochmal spielen"):
        st.session_state.aufgaben=[]
        st.session_state.index=0
        st.session_state.fertig=False
        st.session_state.antwort=""

# -------------------- Fortschritt anzeigen --------------------
st.sidebar.subheader("Erledigt ✅")
if st.sidebar.button("Fortschritt anzeigen"):
    if st.session_state.user in progress:
        for eintrag in progress[st.session_state.user]:
            st.write(f"Fach: {eintrag['fach']}, Aufgabe: {eintrag['frage']}, Deine Antwort: {eintrag['antwort']}, Lösung: {eintrag['loesung']}")
    else:
        st.info("Noch keine erledigten Aufgaben.")
