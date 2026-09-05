import ollama

response = ollama.chat(
    model="gemma3",
    messages=[
        {
            "role": "user",
            "content": "Describe what you see in this image in simple language.",
            "images": ["camera_capture.jpg"]
        }
    ]
)

print("\nVISIONX AI RESULT:")
print(response["message"]["content"])
