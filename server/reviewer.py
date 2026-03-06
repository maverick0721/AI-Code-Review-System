from vllm import SamplingParams
from server.ensemble import aggregate_outputs
from server.rag import retrieve_context


def generate(model, prompt):

    sampling = SamplingParams(
        temperature=0.2,
        max_tokens=512,
        top_p=0.9
    )

    outputs = model.generate(prompt, sampling)

    return outputs[0].outputs[0].text


def run_review(models, prompt):

    context = retrieve_context(prompt)

    full_prompt = context + "\n" + prompt

    results = []

    for model in models:

        output = generate(model, full_prompt)

        results.append(output)

    final = aggregate_outputs(results)

    return final