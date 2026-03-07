import json
from datetime import datetime

def generate_report(results, repo):

    report = {
        "repository": repo,
        "generated_at": datetime.utcnow().isoformat(),
        "issues": results
    }

    with open("report.json", "w") as f:
        json.dump(report, f, indent=2)

    return report