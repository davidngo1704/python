import os
from huggingface_hub import hf_hub_download
from llama_cpp import Llama
import json
import multiprocessing

threads = multiprocessing.cpu_count()

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
        n_ctx=8192,
        n_threads=threads,
        n_gpu_layers=16,
        chat_format="chatml-function-calling",
        use_mmap=True,
        use_mlock=False,
        verbose=False,
    )


def get_weather(location, unit="C"):
    return {
        "location": location,
        "temperature": 28,
        "unit": unit,
        "condition": "Sunny"
    }

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

    if "tool_calls" in message:
        for call in message["tool_calls"]:
            fn_name = call["function"]["name"]
            raw_args = call["function"]["arguments"]
            args = json.loads(raw_args) if isinstance(raw_args, str) else raw_args

            if fn_name == "get_weather":
                return get_weather(**args)

        return {"error": "No matching tool."}

    return message["content"]