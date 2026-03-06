import json


def aggregate_outputs(outputs):

    parsed = []

    for out in outputs:

        try:
            parsed.append(json.loads(out))
        except:
            parsed.append({"raw": out})

    return {
        "ensemble_size": len(outputs),
        "results": parsed
    }