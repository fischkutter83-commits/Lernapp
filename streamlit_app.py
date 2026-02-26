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
    "antwort": "",
    "button_pruefen": False,
    "punkte": 0
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
    while len(aufgaben) < anzahl:
        thema = random.choice(themen)
        frage, loesung = "", ""
        if thema=="Addition":
            a,b=random.randint(1,50),random.randint(1,50)
            frage,f"{a} + {b}",str(a+b)
        elif thema=="Subtraktion":
            a,b=random.randint(1,50),random.randint(1,30)
            frage,f"{a} - {b}",str(a-b)
        elif thema=="Multiplikation":
            a,b=random.randint(2,12),random.randint(2,12)
            frage,f"{a} × {b}",str(a*b)
        elif thema=="Division":
            b=random.randint(2,12)
            ergebnis=random.randint(2,12)
            a=b*ergebnis
            frage,f"{a} ÷ {b}",str(ergebnis)
        elif thema=="Bruchrechnung":
            a,b,c,d=[random.randint(1,9) for _ in range(4)]
            f1,f2=fractions.Fraction(a,b),fractions.Fraction(c,d)
            frage=f"{a}/{b} + {c}/{d}"
            loesung=str(f1+f2)
        elif thema=="Prozentrechnung":
            x=random.randint(10,200)
            p=random.randint(5,50)
            frage=f"{p}% von {x}"
            loesung=str(round(x*p/100,2))
        elif thema=="Flächenberechnung":
            l=random.randint(1,20)
            b=random.randint(1,20)
            frage=f"Rechteck: Länge={l}, Breite={b}. Fläche?"
            loesung=str(l*b)
        if frage and frage not in [f[0] for f in aufgaben]:
            aufgaben.append((frage,loesung,f"{frage} = {loesung}"))
    return aufgaben

# -------------------- DEUTSCH --------------------
def generiere_deutsch_aufgaben(klasse, anzahl, themen):
    aufgaben=[]
    while len(aufgaben)<anzahl:
        thema=random.choice(themen)
        frage, loesung = "",""
        if thema=="Satzglieder":
            frage="Finde das Subjekt: 'Der Hund läuft im Park.'"
            loesung="Der Hund"
        elif thema=="Kommasetzung":
            frage="Setze Kommas: Ich mag Äpfel Birnen und Bananen."
            loesung="Ich mag Äpfel, Birnen und Bananen."
        elif thema=="Großkleinschreibung":
            frage="Schreibe richtig: der mann geht nach hause."
            loesung="Der Mann geht nach Hause."
        elif thema=="Rechtschreibstrategien":
            frage="Richtig schreiben: Apfel oder Apfel?"
            loesung="Apfel"
        if frage and frage not in [f[0] for f in aufgaben]:
            aufgaben.append((frage,loesung,f"Richtig: {loesung}"))
    return aufgaben

# -------------------- ENGLISCH --------------------
def generiere_englisch_aufgaben(klasse, anzahl, themen):
    aufgaben=[]
    while len(aufgaben)<anzahl:
        thema=random.choice(themen)
        frage, loesung="",""
        if thema=="Vocabulary":
            vocab=[("Hund","dog"),("Katze","cat"),("Haus","house"),("Auto","car")]
            de,en=random.choice(vocab)
            frage=f"Übersetze: {de}"
            loesung=en
        elif thema=="Grammatik":
            grammatik=[("He goes to school","Er geht zur Schule"),("I am happy","Ich bin glücklich")]
            de,en=random.choice(grammatik)
            frage=f"Übersetze: {de}"
            loesung=en
        elif thema=="Zeitformen":
            zeit=[("I went to school","Ich ging zur Schule"),("She is reading","Sie liest gerade")]
            de,en=random.choice(zeit)
            frage=f"Übersetze: {de}"
            loesung=en
        if frage and frage not in [f[0] for f in aufgaben]:
            aufgaben.append((frage,loesung,f"{frage} = {loesung}"))
    return aufgaben

# -------------------- Sidebar --------------------
st.sidebar.write(f"👤 Eingeloggt als: {st.session_state.user}")
fach=st.sidebar.radio("Fach:",["Mathe","Deutsch","Englisch"])
klasse=st.sidebar.slider("Klassenstufe:",1,10,1)
anzahl=st.sidebar.slider("Anzahl Aufgaben:",1,10,5)

# Unterthemen auswählen
if fach=="Mathe":
    unterthemen=st.sidebar.multiselect("Unterthemen Mathe:",["Addition","Subtraktion","Multiplikation","Division","Bruchrechnung","Prozentrechnung","Flächenberechnung"],default=["Addition"])
elif fach=="Deutsch":
    unterthemen=st.sidebar.multiselect("Unterthemen Deutsch:",["Satzglieder","Kommasetzung","Großkleinschreibung","Rechtschreibstrategien"],default=["Satzglieder"])
else:
    unterthemen=st.sidebar.multiselect("Unterthemen Englisch:",["Vocabulary","Grammatik","Zeitformen"],default=["Vocabulary"])

if st.sidebar.button("🧩 Quiz starten"):
    if fach=="Mathe": st.session_state.aufgaben=generiere_mathe_aufgaben(klasse,anzahl,unterthemen)
    elif fach=="Deutsch": st.session_state.aufgaben=generiere_deutsch_aufgaben(klasse,anzahl,unterthemen)
    else: st.session_state.aufgaben=generiere_englisch_aufgaben(klasse,anzahl,unterthemen)
    st.session_state.index=0
    st.session_state.fertig=False
    st.session_state.antwort=""
    st.session_state.punkte=0
    st.rerun()

# -------------------- Quiz Ablauf --------------------
if st.session_state.aufgaben and not st.session_state.fertig:
    frage,loesung,erklaerung=st.session_state.aufgaben[st.session_state.index]
    st.subheader(f"Aufgabe {st.session_state.index+1} / {len(st.session_state.aufgaben)}")
    st.write(frage)
    
    st.session_state.antwort=st.text_input("Deine Antwort:",value=st.session_state.antwort,key="antwort_input",
                                         on_change=lambda: setattr(st.session_state,'button_pruefen',True))
    
    if st.session_state.get("button_pruefen",False):
        if st.session_state.antwort.strip().lower()==loesung.strip().lower():
            st.success("✅ Richtig!")
            st.session_state.punkte +=1
        else:
            st.error("❌ Falsch!")
            st.info(erklaerung)
        progress.setdefault(st.session_state.user,[]).append({
            "fach":fach,
            "frage":frage,
            "deine_antwort":st.session_state.antwort,
            "lösung":loesung
        })
        save_json(PROGRESS_FILE,progress)
        st.session_state.antwort=""
        st.session_state.index+=1
        st.session_state.button_pruefen=False
        if st.session_state.index>=len(st.session_state.aufgaben):
            st.session_state.fertig=True
        st.experimental_rerun()

elif st.session_state.fertig:
    st.success(f"🎉 Quiz beendet! Du hast {st.session_state.punkte} von {len(st.session_state.aufgaben)} Aufgaben richtig.")
    st.progress(st.session_state.punkte/len(st.session_state.aufgaben))
    if st.button("🔁 Nochmal spielen"):
        st.session_state.aufgaben=[]
        st.session_state.index=0
        st.session_state.fertig=False
        st.session_state.antwort=""
        st.session_state.punkte=0
        st.rerun()

# -------------------- Fortschritt --------------------
st.sidebar.subheader("Erledigt ✅")
if st.sidebar.button("Fortschritt anzeigen"):
    user_progress=progress.get(st.session_state.user,[])
    if not user_progress:
        st.info("Noch keine erledigten Aufgaben.")
    else:
        for e in user_progress:
            frage=e.get("frage","❓ Unbekannt")
            antwort=e.get("deine_antwort","—")
            loesung=e.get("lösung","—")
            fach=e.get("fach","—")
            st.write(f"📘 **{fach}**: {frage} → {antwort} (Lösung: {loesung})")
