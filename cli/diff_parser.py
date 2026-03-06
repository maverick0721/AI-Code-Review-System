import subprocess

def extract_diff_context(file_path):

    try:
        result = subprocess.run(
            ["git", "diff", "-U20", file_path],
            capture_output=True,
            text=True
        )

        return result.stdout

    except Exception as e:
        return ""