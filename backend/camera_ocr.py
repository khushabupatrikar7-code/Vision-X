import cv2
import pytesseract
from voice import speak

camera = cv2.VideoCapture(0)

# Ask camera for higher resolution
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

if not camera.isOpened():
    print("Could not open camera")
    exit()

print("VisionX OCR Camera ready.")
print("Press SPACE to read text.")
print("Press Q to quit.")

processing = False

while True:
    success, frame = camera.read()

    if not success:
        print("Could not read camera")
        break

    cv2.imshow("VisionX OCR", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    if key == 32 and not processing:

        processing = True

        filename = "ocr_capture.jpg"

        # Save original camera frame
        cv2.imwrite(filename, frame)

        print("\nImage captured!")
        print("Processing text...")

        try:
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Enlarge image
            gray = cv2.resize(
                gray,
                None,
                fx=2,
                fy=2,
                interpolation=cv2.INTER_CUBIC
            )

            # Improve contrast
            gray = cv2.createCLAHE(
                clipLimit=2.0,
                tileGridSize=(8, 8)
            ).apply(gray)

            # Threshold
            processed = cv2.adaptiveThreshold(
                gray,
                255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                31,
                11
            )

            # Try two OCR modes
            text1 = pytesseract.image_to_string(
                processed,
                config="--psm 6"
            ).strip()

            text2 = pytesseract.image_to_string(
                processed,
                config="--psm 11"
            ).strip()

            # Pick the result with more text
            text = text1 if len(text1) >= len(text2) else text2

            if text:
                print("\nVISIONX OCR RESULT:")
                print(text)

                print("\nSpeaking...")
                speak(text, "male")
            else:
                print("\nNo text detected.")
                speak(
                    "I could not detect any text. Please move the camera closer to the page.",
                    "male"
                )

        except Exception as e:
            print("\nOCR ERROR:")
            print(e)

        finally:
            processing = False
            print("\nReady for next scan.")

camera.release()
cv2.destroyAllWindows()