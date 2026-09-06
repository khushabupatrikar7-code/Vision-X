from faster_whisper import WhisperModel
import sounddevice as sd
import scipy.io.wavfile as wav
import ollama
from voice import speak

print("Loading Whisper...")

model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

print("Whisper ready.")

# -----------------------------
# TARGET LANGUAGE
# -----------------------------

print("\nChoose your language:")
print("1. English")
print("2. Hindi")
print("3. Marathi")
print("4. Bengali")
print("5. Tamil")
print("6. Telugu")
print("7. Kannada")
print("8. Gujarati")

choice = input("\nEnter number: ")

languages = {
    "1": "English",
    "2": "Hindi",
    "3": "Marathi",
    "4": "Bengali",
    "5": "Tamil",
    "6": "Telugu",
    "7": "Kannada",
    "8": "Gujarati"
}

target_language = languages.get(choice)

if not target_language:
    print("Invalid choice.")
    exit()

print(f"\nVisionX will translate everything into {target_language}.")

# -----------------------------
# RECORD
# -----------------------------

sample_rate = 16000
duration = 7

print("\n🎤 Speak now...")

audio = sd.rec(
    int(duration * sample_rate),
    samplerate=sample_rate,
    channels=1,
    dtype="int16"
)

sd.wait()

wav.write("voice_input.wav", sample_rate, audio)

print("Processing speech...")

# -----------------------------
# WHISPER
# -----------------------------

segments, info = model.transcribe(
    "voice_input.wav",
    beam_size=5,
    vad_filter=True,
    condition_on_previous_text=False
)

text = " ".join(
    segment.text for segment in segments
).strip()

print("\nDetected language:", info.language)

print("VISIONX HEARD:")
print(text)

if not text:
    print("No speech detected.")
    exit()

# -----------------------------
# GEMMA TRANSLATION
# -----------------------------

prompt = f"""
Translate the following speech into {target_language}.

Rules:
- Return ONLY the translation.
- Do not explain anything.
- Preserve the original meaning.
- Use natural everyday language.

Speech:
{text}
"""

print("\nTranslating...")

response = ollama.chat(
    model="gemma3",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

translation = response["message"]["content"].strip()

print("\nVISIONX TRANSLATION:")
print(translation)

# -----------------------------
# SPEAK
# -----------------------------

print("\nSpeaking...")

speak(translation, "male")

print("\n✅ Translation complete.")