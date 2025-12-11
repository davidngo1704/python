# main.py
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_id = "Helsinki-NLP/opus-mt-en-vi"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

def translate(text: str):
    # Chuẩn bị input
    inputs = tokenizer(text, return_tensors="pt", padding=True)

    # Sinh với các ràng buộc chống lặp
    outputs = model.generate(
        **inputs,
        max_new_tokens=128,        # giới hạn tokens sinh mới
        num_beams=5,               # beam search tăng ổn định
        early_stopping=True,
        no_repeat_ngram_size=3,    # ngăn lặp 3-gram
        repetition_penalty=1.2,    # phạt token lặp
        length_penalty=1.0,        # điều chỉnh độ dài
        do_sample=False            # bật sampling = False => beam deterministic
    )

    text_out = tokenizer.decode(outputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
    return text_out

if __name__ == "__main__":
    examples = [
        "Hello, how are you today?",
        "Machine translation quality improves significantly with larger datasets.",
        "Auto Tokenizer"
    ]
    for ex in examples:
        print("EN:", ex)
        print("VI:", translate(ex))
        print("-" * 60)
