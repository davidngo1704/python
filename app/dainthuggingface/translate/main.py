from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os

from huggingface_hub import snapshot_download

os.makedirs(local_dir, exist_ok=True)


model_name = "vinai/vinai-translate-en2vi-v2"

local_dir = "./models/vinai-translate-en2vi-v2"

snapshot_download(
    repo_id="vinai/vinai-translate-en2vi-v2",
    local_dir=local_dir,
    local_dir_use_symlinks=False
)



tokenizer = AutoTokenizer.from_pretrained(local_dir, use_fast=False)
model = AutoModelForSeq2SeqLM.from_pretrained(local_dir)

text_en = "Hello, how are you today?"
inputs = tokenizer(text_en, return_tensors="pt")

outputs = model.generate(
    **inputs,
    max_new_tokens=200,
    num_beams=5,
    early_stopping=True
)

print(tokenizer.decode(outputs[0], skip_special_tokens=True))
