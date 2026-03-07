import os
import multiprocessing as mp

mp.set_start_method("spawn", force=True)
os.environ["VLLM_WORKER_MULTIPROC_METHOD"] = "spawn"

# Force V0 and disable the experimental V1 components entirely
os.environ["VLLM_USE_V1"] = "0"
os.environ["VLLM_V1_INPROC"] = "0"

from vllm import LLM

def load_models():

    model = LLM(
        model="TheBloke/Mistral-7B-v0.1-AWQ",
        quantization="awq",
        dtype="float16",
        trust_remote_code=True, # Often needed for modern models 
        enforce_eager=True,          # Bypasses complex CUDA graph capture
        disable_log_stats=True,   # <--- This stops the periodic widget updates
        gpu_memory_utilization=0.75, # Leave room for the system
        tensor_parallel_size=1,       # Ensure single-process
        max_model_len=4096
)

    return [model]