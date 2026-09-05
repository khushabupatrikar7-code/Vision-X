from flask import Flask, request, jsonify
import os
from ai import analyze_image

app = Flask(__name__)


@app.route("/")
def home():
    return "VisionX backend is running!"


@app.route("/upload", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "No image received"}), 400

    image = request.files["image"]

    os.makedirs("received_images", exist_ok=True)

    path = os.path.join("received_images", "latest.jpg")
    image.save(path)

    print("Image received. Asking Gemma 3...")

    description = analyze_image(path)
    
    print("AI:", description)

    return jsonify({
        "message": "Image analyzed successfully!",
        "description": description,
        "path": path
    })


if __name__ == "__main__":
    app.run(debug=True)