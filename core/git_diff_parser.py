import subprocess


def get_git_diff(repo_path="."):

    result = subprocess.run(
        ["git", "diff", "HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )

    return result.stdout


def extract_changed_code(diff_text):

    changed_lines = []

    for line in diff_text.split("\n"):

        if line.startswith("+") and not line.startswith("+++"):
            changed_lines.append(line[1:])

    return "\n".join(changed_lines)