import asyncio
import re
import edge_tts
import os
import subprocess


VOICE_OPTIONS = {
    "male": "en-US-GuyNeural",
    "female": "en-US-JennyNeural"
}


def clean_text(text):
    text = re.sub(r"[*_#`]", "", text)
    text = re.sub(r"[•▪◦]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


async def generate_speech(text, voice_type="male"):
    clean = clean_text(text)

    selected_voice = VOICE_OPTIONS.get(
        voice_type,
        VOICE_OPTIONS["male"]
    )

    output_file = "visionx_speech.mp3"

    communicate = edge_tts.Communicate(
        text=clean,
        voice=selected_voice
    )

    await communicate.save(output_file)

    return output_file


def speak(text, voice_type="male"):
    clean = clean_text(text)

    try:
        output_file = asyncio.run(
            generate_speech(clean, voice_type)
        )

        print(f"Speech generated using {voice_type} voice.")

        subprocess.run(
            ["mpg123", "-q", output_file],
            check=False
        )

    except Exception as e:
        print("Edge TTS unavailable.")
        print("Using local voice instead.")

        subprocess.run(
            ["espeak", "-v", "en-us", clean],
            check=False
        )


if __name__ == "__main__":
    speak(
        "*Hello!* I am VisionX. "
        "If Edge TTS is unavailable, I can still speak.",
        "male"
    )