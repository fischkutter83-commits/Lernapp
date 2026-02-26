import streamlit as st
import random
import fractions
import json
import os
import matplotlib.pyplot as plt

# -------------------- Page Setup --------------------
st.set_page_config(page_title="Lern-App", layout="centered")
st.markdown("<h1 style='text-align:center;'>📚 Lern-App</h1>", unsafe_allow_html=True)
st.markdown("---")

USERS_FILE = "users.json"
PROGRESS_FILE = "progress.json"

# -------------------- JSON Utils --------------------
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
st.session_state.setdefault("user", None)
st.session_state.setdefault("aufgaben", [])
st.session_state.setdefault("index", 0)
st.session_state.setdefault("fertig", False)

# -------------------- LOGIN --------------------
if st.session_state.user is None:
    st.subheader("🔐 Login / Registrierung")

    username = st.text_input("👤 Benutzername")
    password = st.text_input("🔑 Passwort", type="password")

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

# -------------------- Aufgaben Generator --------------------
def generiere_mathe_aufgaben(klasse, anzahl):
    aufgaben = []
    ops = ["Plus", "Minus", "Mal", "Geteilt"] if klasse <= 6 else ["Plus", "Minus", "Mal", "Geteilt", "Bruch", "Potenz"]

    for _ in range(anzahl):
        art = random.choice(ops)

        if art == "Plus":
            a, b = random.randint(1, 50), random.randint(1, 50)
            aufgaben.append((f"{a} + {b}", str(a + b)))

        elif art == "Minus":
            a, b = random.randint(20, 50), random.randint(1, 20)
            aufgaben.append((f"{a} - {b}", str(a - b)))

        elif art == "Mal":
            a, b = random.randint(2, 12), random.randint(2, 12)
            aufgaben.append((f"{a} × {b}", str(a * b)))

        elif art == "Geteilt":
            b = random.randint(2, 12)
            ergebnis = random.randint(2, 12)
            aufgaben.append((f"{b * ergebnis} ÷ {b}", str(ergebnis)))

        elif art == "Bruch":
            f1 = fractions.Fraction(random.randint(1, 9), random.randint(1, 9))
            f2 = fractions.Fraction(random.randint(1, 9), random.randint(1, 9))
            aufgaben.append((f"{f1} + {f2}", str(f1 + f2)))

        elif art == "Potenz":
            a, b = random.randint(2, 9), random.randint(2, 4)
            aufgaben.append((f"{a}^{b}", str(a ** b)))

    return aufgaben

# -------------------- Sidebar --------------------
st.sidebar.markdown("## ⚙️ Einstellungen")
st.sidebar.write(f"👤 **{st.session_state.user}**")

klasse = st.sidebar.slider("🎓 Klassenstufe", 1, 10, 1)
anzahl = st.sidebar.slider("🧩 Anzahl Aufgaben", 1, 10, 5)

if st.sidebar.button("▶ Quiz starten"):
    st.session_state.aufgaben = generiere_mathe_aufgaben(klasse, anzahl)
    st.session_state.index = 0
    st.session_state.fertig = False
    st.rerun()

# -------------------- Quiz Ablauf --------------------
if st.session_state.aufgaben and not st.session_state.fertig:
    frage, loesung = st.session_state.aufgaben[st.session_state.index]

    st.markdown(f"### 🧠 Aufgabe {st.session_state.index + 1}")
    st.info(frage)

    antwort = st.text_input("✍️ Deine Antwort")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Antwort prüfen"):
            richtig = antwort.strip().lower() == loesung.lower()

            if richtig:
                st.success("✅ Richtig!")
            else:
                st.error(f"❌ Falsch – Lösung: {loesung}")

            progress.setdefault(st.session_state.user, []).append({
                "richtig": richtig
            })
            save_json(PROGRESS_FILE, progress)

    with col2:
        if st.button("➡️ Nächste Aufgabe"):
            st.session_state.index += 1
            if st.session_state.index >= len(st.session_state.aufgaben):
                st.session_state.fertig = True
            st.rerun()

# -------------------- Ergebnis + Kreisdiagramm --------------------
if st.session_state.fertig:
    st.success("🎉 Quiz beendet!")

    user_progress = progress.get(st.session_state.user, [])
    richtig = sum(1 for e in user_progress if e["richtig"])
    falsch = len(user_progress) - richtig

    st.markdown("## 📊 Dein Ergebnis")

    fig, ax = plt.subplots()
    ax.pie(
        [richtig, falsch],
        labels=["Richtig", "Falsch"],
        autopct="%1.1f%%",
        startangle=90
    )
    ax.axis("equal")

    st.pyplot(fig)

    if st.button("🔁 Nochmal spielen"):
        st.session_state.aufgaben = []
        st.session_state.index = 0
        st.session_state.fertig = False
        st.rerun()
