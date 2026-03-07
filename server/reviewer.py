from vllm import SamplingParams
from server.ensemble import aggregate_outputs
from server.rag import retrieve_context


from vllm import SamplingParams


from vllm import SamplingParams

def generate(model, prompt):

    sampling = SamplingParams(
        temperature=0.0,
        max_tokens=200,
        top_p=0.9,
        stop=["\n\n"]
    )

    structured_prompt = f"""
You are an AI security code reviewer.

Return ONLY a valid JSON object.

Do not add explanations outside JSON.

Format:

{{
  "issue": "<category>",
  "severity": "<low|medium|high|critical>",
  "confidence": <0-1>,
  "explanation": "<short explanation>"
}}

Categories:
hardcoded credential
sql injection
command injection
path traversal
insecure randomness
unsafe deserialization
weak crypto
eval injection
insecure temp file
sensitive data exposure
insecure ssl
unsafe file handling
none

Code:
{prompt}

JSON:
"""

    outputs = model.generate([structured_prompt], sampling)

    return outputs[0].outputs[0].text.strip()

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