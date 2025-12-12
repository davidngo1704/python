import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

from ..translate.main import dich_tieng_viet_sang_tieng_anh

MODEL_ID = "valpy/prompt-classification"
LOCAL_DIR = "./models/valpy_prompt_classification"


def load_prompt_classifier():
    """
    Load model from local folder if exists.
    If not, download from HF and save to local.
    """
    if os.path.exists(LOCAL_DIR):
        print("🔍 Found local model. Loading from:", LOCAL_DIR)
        tokenizer = AutoTokenizer.from_pretrained(LOCAL_DIR)
        model = AutoModelForSequenceClassification.from_pretrained(LOCAL_DIR)
    else:
        print("⬇️ Local model not found. Downloading from Hugging Face...")
        tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_ID)

        os.makedirs(LOCAL_DIR, exist_ok=True)
        tokenizer.save_pretrained(LOCAL_DIR)
        model.save_pretrained(LOCAL_DIR)

        print("✅ Model downloaded and saved to:", LOCAL_DIR)

    return pipeline(
        "text-classification",
        model=model,
        tokenizer=tokenizer,
        return_all_scores=False
    )


if __name__ == "__main__":
    classifier = load_prompt_classifier()

    # Test prompt
    prompt = "hôm nay bạn thế nào"

    data = dich_tieng_viet_sang_tieng_anh(prompt)

    print("\n📌 tiếng anh:", data)

    result = classifier(data)
    print("\n📌 kết quả phân loại:", result)
