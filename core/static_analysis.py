import subprocess
import json


def run_bandit(path):

    try:
        result = subprocess.run(
            ["bandit", "-r", path, "-f", "json"],
            capture_output=True,
            text=True
        )

        return json.loads(result.stdout)

    except:
        return {}


def run_ruff(path):

    try:
        result = subprocess.run(
            ["ruff", "check", path, "--output-format", "json"],
            capture_output=True,
            text=True
        )

        return json.loads(result.stdout)

    except:
        return {}


def run_semgrep(path):

    try:
        result = subprocess.run(
            ["semgrep", "--json", path],
            capture_output=True,
            text=True
        )

        return json.loads(result.stdout)

    except:
        return {}