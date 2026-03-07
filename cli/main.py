import typer
from rich import print

from cli.chunker import chunk_code
from cli.prompt_builder import build_prompt
from cli.client import send_for_review

from core.git_diff_parser import get_git_diff, extract_changed_code


def review(path: str = "."):
    """Run AI code review on changed git diff."""

    print("[bold green]Starting AI Code Review[/bold green]")

    diff = get_git_diff(path)

    changed_code = extract_changed_code(diff)

    if not changed_code.strip():
        print("No changed lines detected.")
        return

    chunks = chunk_code(changed_code)

    for i, chunk in enumerate(chunks):

        print(f"\n[cyan]Reviewing diff chunk {i+1}/{len(chunks)}[/cyan]")

        prompt = build_prompt("git_diff", chunk)

        result = send_for_review(prompt)

        print(result)


if __name__ == "__main__":
    typer.run(review)