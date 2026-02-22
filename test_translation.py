import requests
from config import OPENROUTER_API_KEY

MODEL = "upstage/solar-pro-3:free"

test_sentences = [
    "Hello, how are you?",
    "The weather is nice today.",
    "I am learning how to use the OpenRouter API.",
]

def translate_to_korean(text: str) -> str:
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a translator. Translate the user's English text to Korean. Reply with only the translated text, no explanation.",
                },
                {"role": "user", "content": text},
            ],
        },
    )
    result = response.json()
    if "error" in result:
        raise RuntimeError(f"API 오류: {result['error']}")
    return result["choices"][0]["message"]["content"].strip()


if __name__ == "__main__":
    print(f"모델: {MODEL}\n")
    print("=" * 50)
    for sentence in test_sentences:
        translated = translate_to_korean(sentence)
        print(f"[EN] {sentence}")
        print(f"[KO] {translated}")
        print("-" * 50)
