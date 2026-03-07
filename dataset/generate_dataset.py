import subprocess
import json
import os
from pathlib import Path

DATASET_FILE = "dataset/security_dataset.json"
os.makedirs("dataset", exist_ok=True)

repos = [
    "https://github.com/pallets/flask",
    "https://github.com/psf/requests",
    "https://github.com/fastapi/fastapi"
]


def clone_repo(url):

    name = url.split("/")[-1]

    if not os.path.exists(name):
        subprocess.run(["git", "clone", "--depth", "1", url])


def scan_repo(repo):

    result = subprocess.run(
        ["bandit", "-r", repo, "-f", "json"],
        capture_output=True,
        text=True
    )

    try:
        return json.loads(result.stdout)
    except:
        return None


def extract_samples(scan_output, repo):

    samples = []

    if not scan_output:
        return samples

    for issue in scan_output.get("results", []):

        file_path = issue["filename"]

        try:
            with open(file_path) as f:
                code = f.read()
        except:
            continue

        samples.append({
            "repo": repo,
            "file": file_path,
            "code": code,
            "issue": issue["issue_text"]
        })

    return samples


def main():

    dataset = []

    for repo in repos:

        clone_repo(repo)

        name = repo.split("/")[-1]

        scan = scan_repo(name)

        samples = extract_samples(scan, name)

        dataset.extend(samples)

    with open(DATASET_FILE, "w") as f:
        json.dump(dataset, f, indent=2)


if __name__ == "__main__":
    main()