import asyncio
import re
import edge_tts
import os


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
    output_file = asyncio.run(
        generate_speech(text, voice_type)
    )

    print(f"Speech generated using {voice_type} voice.")

    os.system(f"mpg123 -q '{output_file}'")


if __name__ == "__main__":
    speak(
        "Hello. I am VisionX.",
        "male"
    )