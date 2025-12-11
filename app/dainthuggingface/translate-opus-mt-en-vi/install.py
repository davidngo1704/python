from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os

from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="Helsinki-NLP/opus-mt-en-vi",
    local_dir="./models/opus-mt-en-vi",
    local_dir_use_symlinks=False
)
