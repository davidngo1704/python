import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from ..translate.main import dich_tieng_viet_sang_tieng_anh

MODEL_ID = "reddgr/zero-shot-prompt-classifier-bart-ft"
LOCAL_DIR = "./models/zero_shot_prompt_classifier_bart_ft"


def load_prompt_classifier():
    """
    Load model locally if exists.
    Otherwise download from HF and save to local folder.
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
    prompt = "viết hàm tính tổng bằng python."
    data = dich_tieng_viet_sang_tieng_anh(prompt)

    print("\n📌 Prompt:", data)
    
    result = classifier(data)

    print("\n📌 Kết quả phân loại:", result)
