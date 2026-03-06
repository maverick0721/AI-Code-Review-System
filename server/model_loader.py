from vllm import LLM


def load_models():

    model = LLM(
        model="meta-llama/Meta-Llama-3-8B-Instruct",
        tensor_parallel_size=1,
        gpu_memory_utilization=0.9,
        max_model_len=4096
    )

    return [model]