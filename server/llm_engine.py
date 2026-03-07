from server.model_loader import load_models

models = load_models()


def run_llm(prompt):

    outputs = models[0].generate(
        prompt,
        max_tokens=256
    )

    return outputs[0].outputs[0].text


def run_llm_batch(prompts):

    outputs = models[0].generate(
        prompts,
        max_tokens=256
    )

    results = []

    for out in outputs:
        results.append(out.outputs[0].text)

    return results