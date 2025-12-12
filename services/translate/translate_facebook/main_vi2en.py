import os
from transformers import MBart50TokenizerFast, MBartForConditionalGeneration

MODEL_ID = "facebook/mbart-large-50-many-to-many-mmt"
LOCAL_DIR = "./models/mbart50"

# 1. Load model & tokenizer
def load_model():
    if not os.path.exists(LOCAL_DIR):
        print("Model chưa có trong thư mục local. Tiến hành tải...")
        tokenizer = MBart50TokenizerFast.from_pretrained(MODEL_ID)
        model = MBartForConditionalGeneration.from_pretrained(MODEL_ID)

        tokenizer.save_pretrained(LOCAL_DIR)
        model.save_pretrained(LOCAL_DIR)
        print("Tải xong và đã lưu vào", LOCAL_DIR)
    else:
        print("Đã tìm thấy model local, load offline...")
        tokenizer = MBart50TokenizerFast.from_pretrained(LOCAL_DIR)
        model = MBartForConditionalGeneration.from_pretrained(LOCAL_DIR)

    return tokenizer, model


# 2. Hàm dịch từ tiếng Việt → tiếng Anh
def translate_vi_en(text, tokenizer, model):
    tokenizer.src_lang = "vi_VN"

    inputs = tokenizer(text, return_tensors="pt")

    generated = model.generate(
        **inputs,
        forced_bos_token_id=tokenizer.lang_code_to_id["en_XX"],  # output EN
        max_new_tokens=200,
        num_beams=5,
        early_stopping=True
    )

    return tokenizer.decode(generated[0], skip_special_tokens=True)


# Chạy thử
if __name__ == "__main__":
    tokenizer, model = load_model()

    examples = [
        "hệ điều hành linux là gì?",
    ]

    for ex in examples:
        print("\nVI:", ex)
        print("EN:", translate_vi_en(ex, tokenizer, model))
        print("-" * 60)
