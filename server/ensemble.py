import json


def aggregate_outputs(outputs):

    parsed_results = []

    for out in outputs:

        try:
            parsed = json.loads(out)
        except:
            parsed = {
                "issue": "unknown",
                "severity": "low",
                "confidence": 0.0,
                "explanation": out
            }

        parsed_results.append(parsed)

    return {
        "results": parsed_results
    }