from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_id = "Helsinki-NLP/opus-mt-en-vi"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

text = "tokenizer"

inputs = tokenizer(text, return_tensors="pt")

outputs = model.generate(
    **inputs,
    max_length=256
)

result = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(result)
