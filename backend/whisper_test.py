from faster_whisper import WhisperModel
import sounddevice as sd
import scipy.io.wavfile as wav

print("Loading Whisper...")

model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

print("Whisper ready.")
print("Speak for 5 seconds...")

sample_rate = 16000
duration = 5

audio = sd.rec(
    int(duration * sample_rate),
    samplerate=sample_rate,
    channels=1,
    dtype="int16"
)

sd.wait()

wav.write("voice_input.wav", sample_rate, audio)

print("Processing speech...")

segments, info = model.transcribe(
    "voice_input.wav",
    language="hi",
    beam_size=5,
vad_filter=True,
condition_on_previous_text=False
)
text = " ".join(segment.text for segment in segments).strip()

print("Detected language:", info.language)
print("Confidence:", info.language_probability)

print("\nVISIONX HEARD:")
print(text)