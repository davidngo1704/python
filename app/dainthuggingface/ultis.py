import os
from huggingface_hub import hf_hub_download
from llama_cpp import Llama

MODEL_REPO = "Qwen/Qwen2.5-1.5B-Instruct-GGUF"
MODEL_FILE = "qwen2.5-1.5b-instruct-q4_k_m.gguf"
MODEL_DIR = "models"

def ensure_local_model():

    current_dir = os.path.dirname(os.path.abspath(__file__))

    models_path = os.path.join(current_dir, MODEL_DIR)
    
    os.makedirs(models_path, exist_ok=True)

    local_model_path = os.path.join(models_path, MODEL_FILE)

    if os.path.exists(local_model_path):
        return local_model_path

    downloaded_path = hf_hub_download(
        repo_id=MODEL_REPO,
        filename=MODEL_FILE,
        local_dir=models_path,
        local_dir_use_symlinks=False,
    )

    return downloaded_path


def load_llm(model_path):

    return Llama(
        model_path=model_path,
        n_ctx=4096,
        n_threads=8,
        n_gpu_layers=0,
        chat_format="chatml",
        verbose=False,
    )


def chat(system_promt, input_text):
    llm = load_llm(ensure_local_model())

    resp = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": system_promt},
            {"role": "user", "content": input_text},
        ],
        max_tokens=400,
        temperature=0.6,
        top_p=0.9,
    )

    return resp["choices"][0]["message"]["content"]
