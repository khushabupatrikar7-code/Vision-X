import ollama

def translate(text, target_language="Marathi"):
    prompt = f"""
Translate the following text into {target_language}.

Rules:
- Return ONLY the translation.
- Do not explain anything.
- Preserve the meaning.
- Use natural everyday language.

Text:
{text}
"""

    response = ollama.chat(
        model="gemma3",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"].strip()


if __name__ == "__main__":
    text = input("Enter text: ")

    result = translate(text, "Marathi")

    print("\nVISIONX TRANSLATION:")
    print(result)