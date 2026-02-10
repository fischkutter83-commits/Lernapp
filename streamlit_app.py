import streamlit as st
import random

st.set_page_config(page_title="Einfache Lern-App")
st.title("📘 Einfache Lern-App")

# ---------------- Fach auswählen ----------------
fach = st.selectbox("Wähle ein Fach:", ["Mathe", "Englisch"])

# ---------------- Aufgaben ----------------
if fach == "Mathe":
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    frage = f"{a} + {b}"
    loesung = str(a + b)

else:
    vokabeln = {
        "rot": "red",
        "blau": "blue",
        "Hund": "dog"
    }
    wort, loesung = random.choice(list(vokabeln.items()))
    frage = f"Übersetze: {wort}"

# ---------------- Anzeige ----------------
st.subheader("📝 Aufgabe")
st.write(frage)

antwort = st.text_input("Deine Antwort")

if st.button("Antwort prüfen"):
    if antwort.strip().lower() == loesung.lower():
        st.success("✅ Richtig!")
    else:
        st.error("❌ Falsch")
        st.info(f"Richtige Antwort: **{loesung}**")
