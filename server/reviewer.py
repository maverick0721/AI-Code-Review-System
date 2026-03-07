from vllm import SamplingParams
from server.ensemble import aggregate_outputs
from server.rag import retrieve_context
from core.static_analysis import run_bandit, run_semgrep, run_ruff

import json
import re


def extract_json(text):
    """
    Extract valid JSON from model output.
    Prevents failures if the model outputs extra text.
    """

    try:
        return json.loads(text)

    except Exception:
        match = re.search(r"\{.*\}", text, re.DOTALL)

        if match:
            try:
                return json.loads(match.group())
            except Exception:
                pass

    return {
        "issue": "unknown",
        "severity": "low",
        "confidence": 0.0,
        "explanation": "model output parsing failed"
    }

def rule_based_scan(code):

    rules = []

    if "password =" in code or "passwd =" in code:
        rules.append("hardcoded credential")

    if "eval(" in code:
        rules.append("eval injection")

    if "os.system(" in code:
        rules.append("command injection")

    if "subprocess" in code and "shell=True" in code:
        rules.append("command injection")

    if "../" in code:
        rules.append("path traversal")

    if "random.random()" in code:
        rules.append("insecure randomness")

    if "pickle.loads" in code:
        rules.append("unsafe deserialization")

    return rules

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

    raw_output = outputs[0].outputs[0].text.strip()

    return extract_json(raw_output)


def run_review(models, prompt):

    # Run static analysis tools
    static_results = {
        "bandit": run_bandit(prompt),
        "ruff": run_ruff(prompt),
        "semgrep": run_semgrep(prompt)
    }

    # Retrieve RAG security context
    rag_context = retrieve_context(prompt)

    rule_results = rule_based_scan(prompt)

    static_context = f"""
    Rule-based findings:
    {rule_results}

    Static analysis findings:

    Bandit:
    {static_results["bandit"]}

    Ruff:
    {static_results["ruff"]}

    Semgrep:
    {static_results["semgrep"]}
    """

    # Combine all context
    full_prompt = rag_context + "\n" + static_context + "\n" + prompt

    results = []

    # Run ensemble inference
    for model in models:

        output = generate(model, full_prompt)

        results.append(output)

    # Aggregate ensemble outputs
    return aggregate_outputs(results)