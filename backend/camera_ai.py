import cv2
import requests
import time

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Could not open camera")
    exit()

print("Camera is ready.")
print("Press SPACE to capture an image.")
print("Press Q to quit.")

while True:
    success, frame = camera.read()

    if not success:
        print("Could not read camera")
        break

    cv2.imshow("VisionX Camera", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    if key == 32:  # SPACE
        filename = "camera_capture.jpg"
        cv2.imwrite(filename, frame)

        print("Image captured!")
        print("Sending image to VisionX AI...")

        with open(filename, "rb") as image:
            response = requests.post(
                "http://127.0.0.1:5000/upload",
                files={"image": image}
            )

        print("\nVISIONX AI RESULT:")
        print(response.json()["description"])
        print()

        time.sleep(1)

camera.release()
cv2.destroyAllWindows()