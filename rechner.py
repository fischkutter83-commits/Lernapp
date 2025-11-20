import streamlit as st
import random
import fractions

st.title("Lern-App")

# -------------------- Fachwahl --------------------
fach = st.selectbox("Wähle ein Fach:", ["Mathe", "Deutsch", "Englisch"])

# -------------------- Mathe --------------------
if fach == "Mathe":
    st.subheader("Mathe-Menü")
    option = st.radio("Wähle:", ["Rechner", "Übungsaufgaben"])

    if option == "Rechner":
        rechenart = st.selectbox("Wähle Rechenart:", ["Plus", "Minus", "Mal", "Geteilt"])
        zahlen_eingabe = st.text_input("Gib die Zahlen durch Leerzeichen getrennt ein:")
        if st.button("Berechnen") and zahlen_eingabe:
            zahlen = list(map(float, zahlen_eingabe.split()))
            if rechenart == "Plus":
                ergebnis = sum(zahlen)
                st.write(" + ".join(map(str, zahlen)), "=", ergebnis)
            elif rechenart == "Minus":
                ergebnis = zahlen[0]
                for z in zahlen[1:]:
                    ergebnis -= z
                st.write(" - ".join(map(str, zahlen)), "=", ergebnis)
            elif rechenart == "Mal":
                ergebnis = 1
                for z in zahlen:
                    ergebnis *= z
                st.write(" × ".join(map(str, zahlen)), "=", ergebnis)
            elif rechenart == "Geteilt":
                ergebnis = zahlen[0]
                for z in zahlen[1:]:
                    ergebnis /= z
                st.write(" ÷ ".join(map(str, zahlen)), "=", ergebnis)

    elif option == "Übungsaufgaben":
        klasse = st.slider("Wähle deine Klassenstufe:", 1, 10, 1)
        if klasse <= 2:
            operationen = ["+", "-"]
        elif klasse <= 6:
            operationen = ["+", "-", "*", "/"]
        else:
            operationen = ["+", "-", "*", "/", "bruch", "potenz"]

        aufgabe = st.selectbox("Welche Aufgabe möchtest du üben?", operationen)
        if st.button("Aufgabe anzeigen"):
            if aufgabe == "+":
                a, b = random.randint(1, 20), random.randint(1, 20)
                st.write(f"{a} + {b} = ?")
                antwort = st.text_input("Deine Antwort für Plus:")
                if antwort:
                    richtig = a + b
                    if antwort.strip() == str(richtig):
                        st.success("✅ Richtig!")
                    else:
                        st.error(f"❌ Falsch! Richtige Antwort: {richtig}")

            elif aufgabe == "-":
                a, b = random.randint(1, 20), random.randint(1, 20)
                st.write(f"{a} - {b} = ?")
                antwort = st.text_input("Deine Antwort für Minus:")
                if antwort:
                    richtig = a - b
                    if antwort.strip() == str(richtig):
                        st.success("✅ Richtig!")
                    else:
                        st.error(f"❌ Falsch! Richtige Antwort: {richtig}")

            elif aufgabe == "*":
                a, b = random.randint(1, 12), random.randint(1, 12)
                st.write(f"{a} × {b} = ?")
                antwort = st.text_input("Deine Antwort für Mal:")
                if antwort:
                    richtig = a * b
                    if antwort.strip() == str(richtig):
                        st.success("✅ Richtig!")
                    else:
                        st.error(f"❌ Falsch! Richtige Antwort: {richtig}")

            elif aufgabe == "/":
                b = random.randint(1, 10)
                a = b * random.randint(1, 10)
                st.write(f"{a} ÷ {b} = ?")
                antwort = st.text_input("Deine Antwort für Geteilt:")
                if antwort:
                    richtig = a // b
                    if antwort.strip() == str(richtig):
                        st.success("✅ Richtig!")
                    else:
                        st.error(f"❌ Falsch! Richtige Antwort: {richtig}")

            elif aufgabe == "bruch" and klasse >= 7:
                a, b = random.randint(1, 9), random.randint(1, 9)
                c, d = random.randint(1, 9), random.randint(1, 9)
                st.write(f"{a}/{b} + {c}/{d} = ? (Antwort als gekürzter Bruch z.B. 3/4)")
                antwort = st.text_input("Deine Antwort für Bruch:")
                if antwort:
                    richtig = fractions.Fraction(a, b) + fractions.Fraction(c, d)
                    if antwort.strip() == str(richtig):
                        st.success("✅ Richtig!")
                    else:
                        st.error(f"❌ Falsch! Richtige Antwort: {richtig}")

            elif aufgabe == "potenz" and klasse >= 7:
                a, b = random.randint(2, 9), random.randint(2, 4)
                st.write(f"{a}^{b} = ?")
                antwort = st.text_input("Deine Antwort für Potenz:")
                if antwort:
                    richtig = a ** b
                    if antwort.strip() == str(richtig):
                        st.success("✅ Richtig!")
                    else:
                        st.error(f"❌ Falsch! Richtige Antwort: {richtig}")

# -------------------- Deutsch --------------------
elif fach == "Deutsch":
    st.subheader("Deutsch Aufgaben")
    klasse = st.slider("Wähle deine Klassenstufe:", 1, 10, 1)
    if klasse <= 2:
        themen = ["Groß- und Kleinschreibung", "Silben trennen", "Plural"]
    elif klasse <= 4:
        themen = ["Wortarten", "Satzbau", "Reime"]
    elif klasse <= 6:
        themen = ["Rechtschreibung", "Zeitformen", "Synonyme"]
    elif klasse <= 8:
        themen = ["Satzarten", "Kommasetzung", "Fremdwörter"]
    else:
        themen = ["Stilmittel", "Zusammenfassung", "Argumentation"]

    thema = st.selectbox("Welches Thema möchtest du üben?", themen)
    if st.button("Aufgabe anzeigen Deutsch"):
        if thema == "Plural":
            wörter = {"Hund": "Hunde", "Katze": "Katzen", "Auto": "Autos"}
            wort = random.choice(list(wörter.keys()))
            st.write(f"Bilde den Plural von: {wort}")
            antwort = st.text_input("Deine Antwort für Plural:")
            if antwort:
                if antwort.strip().lower() == wörter[wort].lower():
                    st.success("✅ Richtig!")
                else:
                    st.error(f"❌ Falsch! Richtige Antwort: {wörter[wort]}")

        elif thema == "Wortarten":
            wörter = {"laufen": "Verb", "Haus": "Nomen", "schnell": "Adjektiv"}
            wort = random.choice(list(wörter.keys()))
            st.write(f"Welche Wortart ist '{wort}'?")
            antwort = st.text_input("Deine Antwort für Wortart:")
            if antwort:
                if antwort.strip().lower() == wörter[wort].lower():
                    st.success("✅ Richtig!")
                else:
                    st.error(f"❌ Falsch! Richtige Antwort: {wörter[wort]}")

        elif thema == "Rechtschreibung":
            wörter = {"Fahrrad": "Fahrrad", "spazieren": "spazieren", "Känguru": "Känguru"}
            wort = random.choice(list(wörter.keys()))
            st.write(f"Schreibe das Wort richtig: {wort.lower()}")
            antwort = st.text_input("Deine Antwort für Rechtschreibung:")
            if antwort:
                if antwort.strip() == wort:
                    st.success("✅ Richtig!")
                else:
                    st.error(f"❌ Falsch! Richtige Antwort: {wort}")

        elif thema == "Synonyme":
            wörter = {"schnell": "rasch", "schön": "hübsch", "kalt": "frostig"}
            wort = random.choice(list(wörter.keys()))
            st.write(f"Nenne ein Synonym für: {wort}")
            antwort = st.text_input("Deine Antwort für Synonyme:")
            if antwort:
                if antwort.strip().lower() == wörter[wort].lower():
                    st.success("✅ Richtig!")
                else:
                    st.error(f"❌ Falsch! Richtige Antwort: {wörter[wort]}")

        elif thema == "Stilmittel":
            st.write("Stilmittel erkennen: 'Die Sonne lacht am Himmel.'")
            st.write("a) Metapher  b) Vergleich  c) Alliteration")
            antwort = st.text_input("Deine Antwort (a/b/c):")
            if antwort:
                richtig = "a"
                if antwort.strip().lower() == richtig:
                    st.success("✅ Richtig!")
                else:
                    st.error(f"❌ Falsch! Richtige Antwort: Metapher")

# -------------------- Englisch --------------------
elif fach == "Englisch":
    st.subheader("Englisch Aufgaben")
    klasse = st.slider("Wähle deine Klassenstufe:", 1, 10, 1)
    if klasse <= 2:
        themen = ["Farben", "Zahlen", "Einfache Wörter"]
    elif klasse <= 4:
        themen = ["Wochentage", "Fragen & Antworten", "Satzstellung"]
    elif klasse <= 6:
        themen = ["Präsensformen", "Vokabeln", "Verneinung"]
    elif klasse <= 8:
        themen = ["Simple Past", "Unregelmäßige Verben", "Fragen bilden"]
    else:
        themen = ["Present Perfect", "If-Sätze", "Passive Voice"]

    thema = st.selectbox("Welches Thema möchtest du üben?", themen)
    if st.button("Aufgabe anzeigen Englisch"):
        if thema == "Farben":
            wörter = {"rot": "red", "blau": "blue", "grün": "green"}
            wort = random.choice(list(wörter.keys()))
            st.write(f"Übersetze ins Englische: {wort}")
            antwort = st.text_input("Deine Antwort für Farben:")
            if antwort:
                if antwort.strip().lower() == wörter[wort]:
                    st.success("✅ Richtig!")
                else:
                    st.error(f"❌ Falsch! Richtige Antwort: {wörter[wort]}")

        elif thema == "Zahlen":
            zahl = random.randint(1, 20)
            st.write(f"Wie heißt die Zahl {zahl} auf Englisch?")
            antwort = st.text_input("Deine Antwort für Zahl:")
            numbers = {1:"one",2:"two",3:"three",4:"four",5:"five",6:"six",
                       7:"seven",8:"eight",9:"nine",10:"ten",
                       11:"eleven",12:"twelve",13:"thirteen",14:"fourteen",15:"fifteen",
                       16:"sixteen",17:"seventeen",18:"eighteen",19:"nineteen",20:"twenty"}
            richtig = numbers[zahl]
            if antwort:
                if antwort.strip().lower() == richtig:
                    st.success("✅ Richtig!")
                else:
                    st.error(f"❌ Falsch! Richtige Antwort: {richtig}")

        elif thema == "Einfache Wörter":
            wörter = {"Haus": "house", "Hund": "dog", "Katze": "cat"}
            wort = random.choice(list(wörter.keys()))
            st.write(f"Übersetze ins Englische: {wort}")
            antwort = st.text_input("Deine Antwort für Einfache Wörter:")
            if antwort:
                if antwort.strip().lower() == wörter[wort]:
                    st.success("✅ Richtig!")
                else:
                    st.error(f"❌ Falsch! Richtige Antwort: {wörter[wort]}")

        elif thema == "Wochentage":
            wörter = {"Monday": "Montag", "Tuesday": "Dienstag", "Friday": "Freitag"}
            wort = random.choice(list(wörter.keys()))
            st.write(f"Übersetze ins Deutsche: {wort}")
            antwort = st.text_input("Deine Antwort für Wochentage:")
            if antwort:
                if antwort.strip().lower() == wörter[wort].lower():
                    st.success("✅ Richtig!")
                else:
                    st.error(f"❌ Falsch! Richtige Antwort: {wörter[wort]}")

        elif thema == "Simple Past":
            formen = {"go":"went", "eat":"ate", "see":"saw"}
            verb = random.choice(list(formen.keys()))
            st.write(f"Setze das Verb '{verb}' in Simple Past!")
            antwort = st.text_input("Deine Antwort für Simple Past:")
            if antwort:
                if antwort.strip().lower() == formen[verb]:
                    st.success("✅ Richtig!")
                else:
                    st.error(f"❌ Falsch! Richtige Antwort: {formen[verb]}")
