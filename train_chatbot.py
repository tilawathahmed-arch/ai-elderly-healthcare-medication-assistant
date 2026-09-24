import json
from pathlib import Path
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "data" / "intents.json"
MODEL_DIR = BASE_DIR / "ml" / "model"
MODEL_DIR.mkdir(parents=True, exist_ok=True)


def train():
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    texts, labels, responses = [], [], {}
    for intent in data["intents"]:
        responses[intent["tag"]] = intent["responses"]
        for pattern in intent["patterns"]:
            texts.append(pattern)
            labels.append(intent["tag"])

    model = Pipeline([
        ("tfidf", TfidfVectorizer(lowercase=True, strip_accents="unicode", ngram_range=(1, 2), sublinear_tf=True)),
        ("classifier", LogisticRegression(max_iter=1800, random_state=42)),
    ])
    model.fit(texts, labels)
    joblib.dump(model, MODEL_DIR / "chatbot_pipeline.joblib")
    (MODEL_DIR / "responses.json").write_text(json.dumps(responses, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Chatbot model trained with {len(texts)} examples and {len(responses)} intents.")


if __name__ == "__main__":
    train()
