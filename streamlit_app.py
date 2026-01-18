import streamlit as st
import random

# ------------------ GRUNDEINSTELLUNGEN ------------------
st.set_page_config(page_title="Lern-App", layout="centered")

st.markdown("""
<style>
body {
    background-color: #f0f8ff;
}
.big-title {
    font-size:40px;
    color:#ff6f61;
    text-align:center;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">📚 Lern-App</div>', unsafe_allow_html=True)

# ------------------ SESSION STATE ------------------
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

# ------------------ AUFGABEN ------------------
def mathe_aufgaben(anzahl, thema):
    tasks = []
    for _ in range(anzahl):
        if thema == "Plus":
            a, b = random.randint(1, 50), random.randint(1, 50)
            tasks.append((f"{a} + {b}", a + b, f"{a} + {b} = {a+b}"))
        elif thema == "Mal":
            a, b = random.randint(2, 10), random.randint(2, 10)
            tasks.append((f"{a} × {b}", a * b, f"{a} × {b} = {a*b}"))
    return tasks

# ------------------ SIDEBAR ------------------
st.sidebar.header("⚙️ Einstellungen")

klasse = st.sidebar.slider("Klassenstufe", 1, 10, 4)
fach = st.sidebar.selectbox("Fach", ["Mathe"])

modus = st.sidebar.radio("Modus", ["🔀 Zufall", "📘 Thema"])

thema = "Plus"
if modus == "📘 Thema":
    thema = st.sidebar.selectbox("Thema wählen", ["Plus", "Mal"])

anzahl = st.sidebar.slider("Anzahl Aufgaben", 1, 10, 5)

if st.sidebar.button("▶️ Quiz starten"):
    st.session_state.aufgaben = mathe_aufgaben(anzahl, thema)
    st.session_state.index = 0
    st.session_state.punkte = 0
    st.session_state.feedback = ""
    st.session_state.quiz_aktiv = True

if st.sidebar.button("⛔ Abbrechen"):
    st.session_state.quiz_aktiv = False
    st.session_state.aufgaben = []

# ------------------ QUIZ ------------------
if st.session_state.quiz_aktiv and st.session_state.index < len(st.session_state.aufgaben):
    frage, lösung, erklärung = st.session_state.aufgaben[st.session_state.index]

    st.subheader(f"Aufgabe {st.session_state.index + 1}")
    st.write(frage)

    antwort = st.text_input("Deine Antwort", key=st.session_state.index)

    if st.button("✔️ Prüfen"):
        if antwort.strip() == str(lösung):
            st.session_state.punkte += 1
            st.session_state.feedback = "✅ Richtig!"
        else:
            st.session_state.feedback = f"❌ Falsch! {erklärung}"

        st.session_state.index += 1
        st.experimental_rerun()

    if st.session_state.feedback:
        st.info(st.session_state.feedback)

# ------------------ ERGEBNIS ------------------
elif st.session_state.quiz_aktiv:
    st.success("🎉 Quiz beendet!")
    st.write(f"Richtig: {st.session_state.punkte} von {len(st.session_state.aufgaben)}")
    st.session_state.quiz_aktiv = False
