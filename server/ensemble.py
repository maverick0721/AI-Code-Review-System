import json
import re


def extract_json(text):

    try:
        return json.loads(text)
    except:

        match = re.search(r"\{.*\}", text, re.DOTALL)

        if match:
            try:
                return json.loads(match.group())
            except:
                pass

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