import os
from huggingface_hub import hf_hub_download
from llama_cpp import Llama
import json
import multiprocessing
threads = multiprocessing.cpu_count()

# MODEL_REPO = "Qwen/Qwen2.5-1.5B-Instruct-GGUF"
# MODEL_FILE = "qwen2.5-1.5b-instruct-q4_k_m.gguf"

MODEL_REPO = "bartowski/Qwen2.5-7B-Instruct-GGUF"
MODEL_FILE = "Qwen2.5-7B-Instruct-Q4_K_M.gguf"

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

def load_llm_function_calling(model_path):

    return Llama(
        model_path=model_path,
        n_ctx=8192,                # Hợp lý cho RAM 32GB, ít lỗi
        n_threads=threads,              # i5-10400 có 12 threads
        n_gpu_layers=16,           # GTX 1050 Ti chỉ chịu tối đa ~16 layers
        chat_format="chatml-function-calling",
        use_mmap=True,             # giảm RAM
        use_mlock=False,           # Windows không nên bật mlock
        verbose=False,

    )

def load_llm(model_path):

    return Llama(
        model_path=model_path,
        n_ctx=32768,
        n_threads=threads,
        n_gpu_layers=0,
        chat_format="chatml",
        verbose=False,
    )

def get_weather(location, unit="C"):
    data = {
        "location": location,
        "temperature": 28,
        "unit": unit,
        "condition": "Sunny"
    }
    return data

def call_llm_function(system_prompt, user_input, functions):
    llm = load_llm_function_calling(ensure_local_model())

    response = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ],
        tools=functions,
        tool_choice="auto",
        max_tokens=300
    )

    message = response["choices"][0]["message"]

    # Trường hợp LLM muốn gọi function
    if "tool_calls" in message:
        for call in message["tool_calls"]:
            fn_name = call["function"]["name"]
            raw_args = call["function"]["arguments"]
            args = json.loads(raw_args) if isinstance(raw_args, str) else raw_args

            if fn_name == "get_weather":
                return get_weather(**args)

        return {"error": "No matching tool."}


    # Không phải function call => chỉ text
    return message["content"]

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
