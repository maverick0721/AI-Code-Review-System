import subprocess
import json
import os
import tempfile


def _run_json_command(cmd):
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    if not result.stdout.strip():
        return {}

    return json.loads(result.stdout)


def _with_temp_code_file(code_text, fn):
    fd, temp_path = tempfile.mkstemp(suffix=".py", prefix="review_")
    try:
        with os.fdopen(fd, "w") as f:
            f.write(code_text or "")
        return fn(temp_path)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def run_bandit(code_text):

    try:
        return _with_temp_code_file(
            code_text,
            lambda path: _run_json_command(["bandit", path, "-f", "json"])
        )

    except:
        return {}


def run_ruff(code_text):

    try:
        return _with_temp_code_file(
            code_text,
            lambda path: _run_json_command(["ruff", "check", path, "--output-format", "json"])
        )

    except:
        return {}


def run_semgrep(code_text):

    try:
        return _with_temp_code_file(
            code_text,
            lambda path: _run_json_command(["semgrep", "--json", path])
        )

    except:
        return {}