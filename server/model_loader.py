import os
import multiprocessing as mp
import logging

mp.set_start_method("spawn", force=True)
os.environ["VLLM_WORKER_MULTIPROC_METHOD"] = "spawn"

# Force V0 and disable the experimental V1 components entirely
os.environ["VLLM_USE_V1"] = "0"
os.environ["VLLM_V1_INPROC"] = "0"

from vllm import LLM


logger = logging.getLogger(__name__)


def _model_name():
    return os.getenv("LLM_MODEL", "TheBloke/Mistral-7B-v0.1-AWQ")


def _gpu_mem_utilization():
    try:
        return float(os.getenv("LLM_GPU_MEMORY_UTILIZATION", "0.75"))
    except ValueError:
        logger.warning("Invalid LLM_GPU_MEMORY_UTILIZATION value; defaulting to 0.75")
        return 0.75

def load_models():
    model_name = _model_name()
    logger.info("Initializing vLLM model: %s", model_name)

    try:
        model = LLM(
            model=model_name,
            quantization="awq",
            dtype="float16",
            trust_remote_code=True,
            enforce_eager=True,
            disable_log_stats=True,
            gpu_memory_utilization=_gpu_mem_utilization(),
            tensor_parallel_size=1,
            max_model_len=4096
        )
    except Exception:
        logger.exception("Failed to initialize vLLM model: %s", model_name)
        raise

    return [model]