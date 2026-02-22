import time
import requests
from config import OPENROUTER_API_KEY
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity as cos_sim

TRANSLATE_MODEL = "upstage/solar-pro-3:free"
EMBED_MODEL_NAME = "sentence-transformers/paraphrase-minilm-l6-v2"

_embed_model = None


def _get_embed_model() -> SentenceTransformer:
    global _embed_model
    if _embed_model is None:
        _embed_model = SentenceTransformer(EMBED_MODEL_NAME)
    return _embed_model


def translate_text(text: str, retries: int = 1) -> str:
    for attempt in range(retries + 1):
        resp = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": TRANSLATE_MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are a professional translator. "
                            "Translate the user's text to Korean. "
                            "Preserve the original formatting (paragraphs, line breaks) as much as possible. "
                            "Reply with only the translated text."
                        ),
                    },
                    {"role": "user", "content": text},
                ],
            },
            timeout=30,
        )
        data = resp.json()
        if "error" not in data:
            return data["choices"][0]["message"]["content"].strip()
        if attempt < retries:
            time.sleep(3)
    raise RuntimeError(data["error"].get("message", "번역 API 오류"))


def compute_similarity(original: str, translated: str) -> float:
    """
    paraphrase-MiniLM-L6-v2 임베딩 기반 코사인 유사도 계산.
    원문(영어)와 번역문(한국어)의 의미 보존도를 0.0~1.0 점수로 반환.
    """
    model = _get_embed_model()
    emb_orig = model.encode([original])
    emb_trans = model.encode([translated])
    score = cos_sim(emb_orig, emb_trans)[0][0]
    return round(float(score), 4)
