import cv2
import ollama
import time
from voice import speak

camera = cv2.VideoCapture(0)

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not camera.isOpened():
    print("Could not open camera")
    exit()

print("================================")
print("       VISION-X CAMERA")
print("================================")
print("SPACE = Describe scene")
print("R     = Read text")
print("Q     = Quit")
print("================================")

processing = False


def ask_gemma(filename, mode):

    if mode == "describe":
        prompt = (
            "Describe this image for a visually impaired person. "
            "Focus on important objects, people, surroundings, "
            "and any clearly visible text. "
            "Be concise, useful and natural. "
            "Do not mention formatting symbols."
        )

    elif mode == "read":
        prompt = (
            "Read all clearly visible text in this image. "
            "Return ONLY the text that you can actually read. "
            "Do not describe the image. "
            "Do not guess missing words. "
            "Do not add explanations."
        )

    start_time = time.time()

    response = ollama.chat(
        model="gemma3",
        keep_alive=-1,
        messages=[
            {
                "role": "user",
                "content": prompt,
                "images": [filename]
            }
        ]
    )

    ai_time = time.time() - start_time

    return response["message"]["content"].strip(), ai_time


while True:

    success, frame = camera.read()

    if not success:
        print("Could not read camera")
        break

    cv2.imshow("VisionX Camera", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    # SPACE = Describe
    if key == 32 and not processing:

        processing = True

        filename = "camera_capture.jpg"

        cv2.imwrite(filename, frame)

        print("\n📷 Image captured!")
        print("👁️ VisionX is analyzing the scene...")

        try:
            description, ai_time = ask_gemma(
                filename,
                "describe"
            )

            print(f"\nAI processing time: {ai_time:.2f} seconds")

            print("\nVISIONX:")
            print(description)

            print("\n🔊 Speaking...")
            speak(description, "male")

        except Exception as e:

            print("\nVisionX error:")
            print(e)

        finally:

            processing = False
            print("\nReady.")
            print("SPACE = Describe | R = Read | Q = Quit")


    # R = Read text
    if key == ord("r") and not processing:

        processing = True

        filename = "camera_read.jpg"

        cv2.imwrite(filename, frame)

        print("\n📷 Image captured!")
        print("📖 VisionX is reading the text...")

        try:

            text, ai_time = ask_gemma(
                filename,
                "read"
            )

            print(f"\nAI processing time: {ai_time:.2f} seconds")

            if text:

                print("\nVISIONX READ:")
                print(text)

                print("\n🔊 Speaking...")
                speak(text, "male")

            else:

                print("\nNo readable text found.")

                speak(
                    "I could not read any text.",
                    "male"
                )

        except Exception as e:

            print("\nVisionX error:")
            print(e)

        finally:

            processing = False
            print("\nReady.")
            print("SPACE = Describe | R = Read | Q = Quit")


camera.release()
cv2.destroyAllWindows()