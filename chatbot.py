import json
from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = BASE_DIR / "ml" / "model"
MODEL_FILE = MODEL_DIR / "chatbot_pipeline.joblib"
RESPONSES_FILE = MODEL_DIR / "responses.json"

FALLBACK = (
    "I can help with medication reminders, wellness tracking, sleep, pain, "
    "hydration, and general support. For diagnosis or medication changes, "
    "please contact a qualified healthcare professional."
)


def ensure_model():
    if not MODEL_FILE.exists() or not RESPONSES_FILE.exists():
        from ml.train_chatbot import train
        train()


def get_response(message: str):
    ensure_model()
    model = joblib.load(MODEL_FILE)
    with RESPONSES_FILE.open("r", encoding="utf-8") as f:
        responses = json.load(f)

    cleaned = (message or "").strip()
    if not cleaned:
        return {"intent": "unknown", "confidence": 0.0, "response": FALLBACK}

    probabilities = model.predict_proba([cleaned])[0]
    classes = model.classes_
    best_index = probabilities.argmax()
    intent = str(classes[best_index])
    confidence = float(probabilities[best_index])

    # The demo dataset is intentionally small, so probability scores can be modest even for
    # obvious examples. Keep the threshold low enough for the included demo intents while
    # still providing a fallback for clearly out-of-domain messages.
    if confidence < 0.20:
        return {"intent": "unknown", "confidence": round(confidence, 3), "response": FALLBACK}

    return {
        "intent": intent,
        "confidence": round(confidence, 3),
        "response": responses.get(intent, [FALLBACK])[0],
    }
