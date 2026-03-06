from github import Github
import os

def post_pr_comment(repo_name, pr_number, body):

    token = os.getenv("GITHUB_TOKEN")

    if not token:
        raise ValueError("GITHUB_TOKEN not set")

    g = Github(token)

    repo = g.get_repo(repo_name)

    pr = repo.get_pull(pr_number)

    pr.create_issue_comment(body)