from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

local_dir = "./models/vinai-translate-en2vi-v2"

tokenizer = AutoTokenizer.from_pretrained(local_dir, use_fast=False)

model = AutoModelForSeq2SeqLM.from_pretrained(local_dir)

text = "Hello, how are you?"

inputs = tokenizer(text, return_tensors="pt")

output = model.generate(**inputs)

print(tokenizer.decode(output[0], skip_special_tokens=True))