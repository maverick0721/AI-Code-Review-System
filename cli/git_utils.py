from git import Repo

def get_changed_files(repo_path="."):
    repo = Repo(repo_path)

    changed_files = []

    diffs = repo.index.diff(None)

    for diff in diffs:

        file_path = diff.a_path

        try:
            with open(file_path, "r") as f:
                content = f.read()

            changed_files.append((file_path, content))

        except:
            pass

    return changed_files