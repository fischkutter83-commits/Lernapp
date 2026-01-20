import streamlit as st
import random
import fractions
import json
import os

# ================== DATEIEN ==================
USERS_FILE = "users.json"
PROGRESS_FILE = "progress.json"

# ================== HILFSFUNKTIONEN ==================
def load_json(path, default):
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump(default, f)
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

users = load_json(USERS_FILE, {})
progress = load_json(PROGRESS_FILE, {})

# ================== SEITEN SETUP ==================
st.set_page_config(page_title="Lern-App", layout="centered")
st.title("📚 Lern-App")

# ================== SESSION STATE ==================
if "user" not in st.session_state:
    st.session_state.user = None
if "aufgaben" not in st.session_state:
    st.session_state.aufgaben = []
if "index" not in st.session_state:
    st.session_state.index = 0
if "punkte" not in st.session_state:
    st.session_state.punkte = 0
if "feedback" not in st.session_state:
    st.session_state.feedback = ""
if "quiz_aktiv" not in st.session_state:
    st.session_state.quiz_aktiv = False

# ================== LOGIN ==================
if st.session_state.user is None:
    st.subheader("🔐 Login / Registrierung")

    username = st.text_input("Benutzername")
    password = st.text_input("Passwort", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Einloggen"):
            if username in users and users[username] == password:
                st.session_state.user = username
                st.rerun()
            else:
                st.error("Falsche Daten")

    with col2:
        if st.button("Registrieren"):
            if username in users:
                st.error("Benutzer existiert schon")
            else:
                users[username] = password
                save_json(USERS_FILE, users)
                st.success("Account erstellt – jetzt einloggen")

    st.stop()

# ================== MATHE AUFGABEN ==================
def mathe_aufgaben(klasse, anzahl):
    ops = ["Plus", "Minus"]
    if klasse >= 3:
        ops += ["Mal", "Geteilt"]
    if klasse >= 7:
        ops += ["Bruch", "Potenz"]

    aufgaben = []

    for _ in range(anzahl):
        art = random.choice(ops)

        if art == "Plus":
            a, b = random.randint(1, 50), random.randint(1, 50)
            aufgaben.append((f"{a} + {b}", a + b, f"{a} + {b} = {a+b}"))

        elif art == "Minus":
            a, b = random.randint(20, 60), random.randint(1, 20)
            aufgaben.append((f"{a} - {b}", a - b, f"{a} - {b} = {a-b}"))

        elif art == "Mal":
            a, b = random.randint(2, 12), random.randint(2, 12)
            aufgaben.append((f"{a} × {b}", a * b, f"{a} × {b} = {a*b}"))

        elif art == "Geteilt":
            b = random.randint(2, 12)
            r = random.randint(2, 12)
            a = b * r
            aufgaben.append((f"{a} ÷ {b}", r, f"{a} ÷ {b} = {r}"))

        elif art == "Bruch":
            a, b, c, d = random.randint(1, 9), random.randint(1, 9), random.randint(1, 9), random.randint(1, 9)
            f1, f2 = fractions.Fraction(a, b), fractions.Fraction(c, d)
            aufgaben.append((f"{a}/{b} + {c}/{d}", str(f1 + f2), f"{f1} + {f2} = {f1+f2}"))

        elif art == "Potenz":
            a, b = random.randint(2, 6), random.randint(2, 3)
            aufgaben.append((f"{a}^{b}", a**b, f"{a}^{b} = {a**b}"))

    return aufgaben

# ================== SIDEBAR ==================
st.sidebar.write(f"👤 Eingeloggt als **{st.session_state.user}**")

fach = st.sidebar.selectbox("Fach", ["Mathe"])
klasse = st.sidebar.slider("Klassenstufe", 1, 10, 1)
anzahl = st.sidebar.slider("Anzahl Aufgaben", 1, 10, 5)

if st.sidebar.button("🎮 Zufalls-Quiz starten"):
    st.session_state.aufgaben = mathe_aufgaben(klasse, anzahl)
    st.session_state.index = 0
    st.session_state.punkte = 0
    st.session_state.feedback = ""
    st.session_state.quiz_aktiv = True

# ================== QUIZ ==================
if st.session_state.quiz_aktiv:
    if st.session_state.index < len(st.session_state.aufgaben):
        frage, lösung, erklärung = st.session_state.aufgaben[st.session_state.index]

        st.subheader(f"Aufgabe {st.session_state.index + 1}")
        st.write(frage)

        antwort_key = f"antwort_{st.session_state.index}"
        antwort = st.text_input("Deine Antwort", key=antwort_key)

        if st.button("✔️ Abgeben"):
            richtig = antwort.strip() == str(lösung)

            if richtig:
                st.success("✅ Richtig!")
                st.session_state.punkte += 1
            else:
                st.error("❌ Falsch")
                st.info(erklärung)

            # Fortschritt speichern (FEHLER BEHOBEN)
            if st.session_state.user not in progress:
                progress[st.session_state.user] = []

            progress[st.session_state.user].append({
                "fach": fach,
                "klasse": klasse,
                "frage": frage,
                "deine_antwort": antwort,
                "richtig": richtig
            })
            save_json(PROGRESS_FILE, progress)

            # Vorbereitung nächste Aufgabe
            st.session_state.index += 1
            st.session_state[antwort_key] = ""
            st.rerun()

    else:
        st.success(f"🎉 Fertig! Punkte: {st.session_state.punkte}/{len(st.session_state.aufgaben)}")
        st.session_state.quiz_aktiv = False

# ================== ERLEDIGT / VERLAUF ==================
st.sidebar.markdown("---")
if st.sidebar.button("📊 Erledigt / Verlauf"):
    st.subheader("📚 Dein Lernverlauf")

    daten = progress.get(st.session_state.user, [])
    if not daten:
        st.info("Noch keine Aufgaben gemacht.")
    else:
        for eintrag in daten:
            st.write(
                f"**{eintrag['fach']}** | Klasse {eintrag['klasse']} | "
                f"{'✅' if eintrag['richtig'] else '❌'} | {eintrag['frage']}"
            )
