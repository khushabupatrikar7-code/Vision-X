import pytesseract
from PIL import Image


IMAGE_PATH = "camera_capture.jpg"


def read_text(image_path):
    image = Image.open(image_path)

    text = pytesseract.image_to_string(image)

    return text.strip()


if __name__ == "__main__":
    text = read_text(IMAGE_PATH)

    print("\nVISIONX OCR RESULT:")
    
    if text:
        print(text)
    else:
        print("No text detected.")