import cv2
import pytesseract
from PIL import Image
from voice import speak


camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Could not open camera.")
    exit()

print("Camera is ready.")
print("Press SPACE to capture.")
print("Press Q to quit.")

while True:
    ret, frame = camera.read()

    if not ret:
        print("Could not read camera.")
        break

    cv2.imshow("VisionX - Text Reader", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    if key == 32:  # SPACE
        print("\nImage captured!")

        cv2.imwrite("camera_ocr.jpg", frame)

        image = Image.fromarray(
            cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        )

        text = pytesseract.image_to_string(image).strip()

        print("\nVISIONX OCR RESULT:")

        if text:
            print(text)

            print("\nSpeaking text...")
            speak(text, "male")

        else:
            print("No text detected.")
            speak("I could not detect any text.", "male")

        print("\nPress SPACE to scan again.")
        print("Press Q to quit.")

camera.release()
cv2.destroyAllWindows()