import ollama


def analyze_image(image_path):
    response = ollama.chat(
        model="gemma3",
        messages=[
            {
                "role": "user",
                "content": (
                    "Describe what you see in this image in simple language. "
                    "Focus on people, objects, surroundings, text, and anything "
                    "important for a person wearing smart glasses."
                ),
                "images": [image_path],
            }
        ],
    )

    return response["message"]["content"]