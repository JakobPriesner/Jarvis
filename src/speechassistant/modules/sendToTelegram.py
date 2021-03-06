import re

# Beschreibung
"""
Mit diesem Modul kann man sich Nachrichten per Telegram zuschicken lassen.
Dazu sagt man "Sende <text> an mein Smartphone" oder "Smartphone Nachricht <text>".
"""


def isValid(text):
    text = text.lower()
    if "smartphone" in text and ("nachricht" in text or "sende" in text):
        return True
    else:
        return False


def handle(text, core, skills):
    text = text.lower()
    length = len(text)

    match = re.search("^smartphone nachricht", text)
    if match is not None:
        end = match.end() + 1
        nachricht = text[end:length]

    else:
        liste = re.split("\s", text)
        elements = len(liste)
        if liste[0] == "sende" and liste[elements - 1] == "smartphone":
            nachricht = ""
            for i in range(1, elements):
                if liste[i] == "an" and liste[i + 1] == "mein":
                    break
                else:
                    nachricht += liste[i]
                    nachricht += " "

    if nachricht != "":
        if core.messenger_call:
            core.say("Du hast folgende Nachricht an dich selbst geschrieben:")
        else:
            core.say("Ok, ich sende " + nachricht + " an dein Smartphone")
            core.say("Nachricht an dich:", output="messenger")
        core.say(nachricht, output="messenger")
    else:
        core.say("Ich konnte deine Nachricht nicht heraus filtern")
