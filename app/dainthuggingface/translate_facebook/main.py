import os
from transformers import MBart50TokenizerFast, MBartForConditionalGeneration

MODEL_ID = "facebook/mbart-large-50-many-to-many-mmt"
LOCAL_DIR = "./models/mbart50"

# 1. Load model và tokenizer (tự tải nếu chưa có local)
def load_model():
    if not os.path.exists(LOCAL_DIR):
        print("Model chưa có trong thư mục local. Tiến hành tải...")
        tokenizer = MBart50TokenizerFast.from_pretrained(MODEL_ID)
        model = MBartForConditionalGeneration.from_pretrained(MODEL_ID)

        # Lưu về local để dùng offline
        tokenizer.save_pretrained(LOCAL_DIR)
        model.save_pretrained(LOCAL_DIR)
        print("Tải xong và đã lưu vào", LOCAL_DIR)
    else:
        print("Đã tìm thấy model local, load offline...")
        tokenizer = MBart50TokenizerFast.from_pretrained(LOCAL_DIR)
        model = MBartForConditionalGeneration.from_pretrained(LOCAL_DIR)

    return tokenizer, model


# 2. Hàm dịch EN → VI
def translate_en_vi(text, tokenizer, model):
    # MBART cần set lang code cho input
    tokenizer.src_lang = "en_XX"

    inputs = tokenizer(text, return_tensors="pt")

    # MBART yêu cầu forced_bos_token_id để đặt ngôn ngữ output
    generated = model.generate(
        **inputs,
        forced_bos_token_id=tokenizer.lang_code_to_id["vi_VN"],
        max_new_tokens=200,
        num_beams=5,
        early_stopping=True
    )

    return tokenizer.decode(generated[0], skip_special_tokens=True)


# Chạy thử
if __name__ == "__main__":
    tokenizer, model = load_model()

    examples = [
        "Hello, how are you today?",
        "Machine translation quality improves significantly with larger datasets.",
        "Auto Tokenizer",
        "Transformers provide state-of-the-art natural language processing capabilities."
    ]

    for ex in examples:
        print("\nEN:", ex)
        print("VI:", translate_en_vi(ex, tokenizer, model))
