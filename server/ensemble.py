import json
import re


def extract_json(text):

    matches = re.findall(r"\{.*?\}", text, re.DOTALL)

    for m in matches:
        try:
            return json.loads(m)
        except:
            continue

    return {
        "issue": "unknown",
        "severity": "low",
        "confidence": 0.0,
        "explanation": text
    }


def aggregate_outputs(outputs):

    parsed = []

    for out in outputs:
        parsed.append(extract_json(out))

    return {"results": parsed}