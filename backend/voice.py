import pyttsx3
import re

engine = pyttsx3.init()

engine.setProperty("rate", 150)
engine.setProperty("volume", 1.0)


def speak(text):
    # Remove Markdown symbols before speaking
    clean_text = re.sub(r"[*_#`]", "", text)

    engine.say(clean_text)
    engine.runAndWait()


if __name__ == "__main__":
    speak("VisionX is working. I can describe what I see.")