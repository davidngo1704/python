from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os

from huggingface_hub import snapshot_download


model_name = "vinai/vinai-translate-en2vi-v2"

local_dir = "./models/vinai-translate-en2vi-v2"

snapshot_download(
    repo_id="vinai/vinai-translate-en2vi-v2",
    local_dir=local_dir,
    local_dir_use_symlinks=False
)
