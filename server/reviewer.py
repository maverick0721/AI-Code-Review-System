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


def run_review(models, prompt, static_results):

    rag_context = retrieve_context(prompt)

    static_context = f"""
Static analysis results:

Bandit:
{static_results.get("bandit")}

Ruff:
{static_results.get("ruff")}

Semgrep:
{static_results.get("semgrep")}
"""

    full_prompt = rag_context + "\n" + static_context + "\n" + prompt

    results = []

    for model in models:

        output = generate(model, full_prompt)

        results.append(output)

    return aggregate_outputs(results)