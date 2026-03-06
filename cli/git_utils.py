from git import Repo

def get_changed_files(repo_path="."):
    repo = Repo(repo_path)

    changed_files = []

    changed = [item.a_path for item in repo.index.diff(None)]
    untracked = repo.untracked_files

    files = set(changed + untracked)

    for file_path in files:

        try:
            with open(file_path, "r") as f:
                content = f.read()

            changed_files.append((file_path, content))

        except:
            pass

    return changed_files