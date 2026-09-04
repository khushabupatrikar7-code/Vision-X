import cv2

camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not camera.isOpened():
    print("Could not open camera")
    exit()

success, frame = camera.read()

if success:
    cv2.imwrite("test_image.jpg", frame)
    print("Photo captured successfully!")

else:
    print("Could not capture photo")

camera.release()