from flask import Flask, request, jsonify
import os

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

    return jsonify({
        "message": "Image received successfully!",
        "path": path
    })

if __name__ == "__main__":
    app.run(debug=True)