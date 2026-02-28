import streamlit as st
import random
import json
import os
import pandas as pd

# ============================================================
# ===================== GRUNDEINSTELLUNGEN ===================
# ============================================================

st.set_page_config(
    page_title="Lern-App",
    layout="wide"
)

st.title("📚 Lern-App")

USERS_FILE = "users.json"
PROGRESS_FILE = "progress.json"

# ============================================================
# ===================== JSON FUNKTIONEN ======================
# ============================================================

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

# ============================================================
# ===================== SESSION STATE ========================
# ============================================================

if "user" not in st.session_state:
    st.session_state.user = None
if "aufgaben" not in st.session_state:
    st.session_state.aufgaben = []
if "index" not in st.session_state:
    st.session_state.index = 0
if "fertig" not in st.session_state:
    st.session_state.fertig = False

# ============================================================
# ===================== LOGIN / REGISTRIERUNG ================
# ============================================================

if st.session_state.user is None:
    st.subheader("🔐 Login / Registrierung")

    col1, col2 = st.columns(2)

    with col1:
        username = st.text_input("Benutzername")
        password = st.text_input("Passwort", type="password")

        if st.button("Einloggen"):
            if username in users and users[username]["password"] == password:
                st.session_state.user = username
                st.success("Willkommen 👋")
                st.rerun()
            else:
                st.error("❌ Falsche Zugangsdaten")

    with col2:
        if st.button("Registrieren"):
            if username in users:
                st.error("❌ Benutzer existiert bereits")
            else:
                users[username] = {"password": password}
                save_json(USERS_FILE, users)
                st.success("✅ Account erstellt – bitte einloggen")

    st.stop()

# ============================================================
# ===================== AUFGABENGENERATOREN ==================
# ============================================================

def mathe_aufgaben(thema, klasse, anzahl):
    aufgaben = []

    max_zahl = 20 if klasse <= 3 else 100 if klasse <= 6 else 500

    for _ in range(anzahl):
        if thema == "Addition":
            a, b = random.randint(1, max_zahl), random.randint(1, max_zahl)
            aufgaben.append((f"{a} + {b}", str(a + b)))

        elif thema == "Subtraktion":
            a, b = random.randint(10, max_zahl), random.randint(1, 10)
            aufgaben.append((f"{a} - {b}", str(a - b)))

        elif thema == "Multiplikation":
            a = random.randint(2, 5 if klasse <= 3 else 12)
            b = random.randint(2, 5 if klasse <= 3 else 12)
            aufgaben.append((f"{a} × {b}", str(a * b)))

        elif thema == "Division":
            b = random.randint(2, 10)
            r = random.randint(2, 10)
            aufgaben.append((f"{b*r} ÷ {b}", str(r)))

        elif thema == "Potenzieren" and klasse >= 5:
            a = random.randint(2, 5)
            b = random.randint(2, 4)
            aufgaben.append((f"{a}^{b}", str(a ** b)))

    return aufgaben

def deutsch_aufgaben(thema, klasse, anzahl):
    daten = {
        "Rechtschreibung": {
            1: {"Hant": "Hand", "Hauß": "Haus"},
            4: {"Fahrrat": "Fahrrad", "wierklich": "wirklich"},
            7: {"Interresse": "Interesse", "Standart": "Standard"}
        },
        "Artikel": {
            1: {"___ Hund": "der", "___ Katze": "die"},
            4: {"___ Auto": "das", "___ Blume": "die"},
            7: {"___ Mädchen": "das", "___ Lehrer": "der"}
        },
        "Satzglieder": {
            4: {"Ich ___ den Ball": "werfe"},
            7: {"Der Hund ___ laut": "bellt"}
        },
        "Wortarten": {
            2: {"laufen": "Verb", "Haus": "Nomen"},
            5: {"schön": "Adjektiv", "lesen": "Verb"},
            8: {"weil": "Konjunktion", "schnell": "Adjektiv"}
        }
    }

    stufe = max(k for k in daten[thema] if klasse >= k)
    pool = daten[thema][stufe]

    return [random.choice(list(pool.items())) for _ in range(anzahl)]

def englisch_aufgaben(thema, klasse, anzahl):
    daten = {
        "Vokabeln": {
            1: {"Hund": "dog", "Katze": "cat"},
            4: {"Haus": "house", "Apfel": "apple"},
            7: {"denken": "think", "laufen": "run"}
        },
        "Zeitformen": {
            5: {"I go (Past)": "went", "I see (Past)": "saw"},
            8: {"I have eaten (Infinitive)": "eat"}
        }
    }

    stufe = max(k for k in daten[thema] if klasse >= k)
    pool = daten[thema][stufe]

    return [random.choice(list(pool.items())) for _ in range(anzahl)]

# ============================================================
# ===================== SIDEBAR (AUSWAHL) ====================
# ============================================================

st.sidebar.markdown("## ⚙️ Lern-Einstellungen")
st.sidebar.write(f"👤 **{st.session_state.user}**")
st.sidebar.divider()

fach = st.sidebar.radio("📘 Fach", ["Mathe", "Deutsch", "Englisch"])
klasse = st.sidebar.slider("🎓 Klassenstufe", 1, 10, 3)

unterthemen = {
    "Mathe": ["Addition", "Subtraktion", "Multiplikation", "Division", "Potenzieren"],
    "Deutsch": ["Rechtschreibung", "Artikel", "Satzglieder", "Wortarten"],
    "Englisch": ["Vokabeln", "Zeitformen"]
}

thema = st.sidebar.selectbox("📂 Unterthema", unterthemen[fach])
anzahl = st.sidebar.slider("🧮 Anzahl Aufgaben", 1, 10, 5)

st.sidebar.divider()

if st.sidebar.button("🚀 Quiz starten", use_container_width=True):
    if fach == "Mathe":
        st.session_state.aufgaben = mathe_aufgaben(thema, klasse, anzahl)
    elif fach == "Deutsch":
        st.session_state.aufgaben = deutsch_aufgaben(thema, klasse, anzahl)
    else:
        st.session_state.aufgaben = englisch_aufgaben(thema, klasse, anzahl)

    st.session_state.index = 0
    st.session_state.fertig = False
    st.rerun()

# ============================================================
# ===================== QUIZ BEREICH =========================
# ============================================================

if st.session_state.aufgaben and not st.session_state.fertig:
    frage, loesung = st.session_state.aufgaben[st.session_state.index]

    st.subheader(f"📝 Aufgabe {st.session_state.index + 1}")
    st.markdown(f"### {frage}")

    antwort = st.text_input("Deine Antwort")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Antwort prüfen", use_container_width=True):
            richtig = antwort.strip().lower() == loesung.lower()

            if richtig:
                st.success("✅ Richtig!")
            else:
                st.error(f"❌ Falsch – Lösung: {loesung}")

            progress.setdefault(st.session_state.user, []).append({
                "fach": fach,
                "thema": thema,
                "klasse": klasse,
                "frage": frage,
                "antwort": antwort,
                "lösung": loesung,
                "richtig": richtig
            })
            save_json(PROGRESS_FILE, progress)

    with col2:
        if st.button("➡️ Nächste Aufgabe", use_container_width=True):
            st.session_state.index += 1
            if st.session_state.index >= len(st.session_state.aufgaben):
                st.session_state.fertig = True
            st.rerun()

elif st.session_state.fertig:
    st.success("🎉 Quiz abgeschlossen!")
    if st.button("🔁 Neues Quiz starten"):
        st.session_state.aufgaben = []
        st.session_state.fertig = False
        st.rerun()

# ============================================================
# ===================== FORTSCHRITTS-DIAGRAMME ===============
# ============================================================

st.markdown("---")
st.header("📊 Dein Lernfortschritt")

user_data = progress.get(st.session_state.user, [])

if not user_data:
    st.info("Noch keine Fortschrittsdaten vorhanden.")
else:
    df = pd.DataFrame(user_data)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📘 Aufgaben pro Fach")
        st.bar_chart(df["fach"].value_counts())

    with col2:
        st.subheader("✅ Richtig vs. ❌ Falsch")
        st.bar_chart(df["richtig"].value_counts())

    st.subheader("📈 Lernverlauf")
    df["laufend"] = range(1, len(df) + 1)
    st.line_chart(df["laufend"])

    with st.expander("📋 Details anzeigen"):
        st.dataframe(
            df[["fach", "thema", "klasse", "frage", "antwort", "lösung", "richtig"]],
            use_container_width=True
        )
