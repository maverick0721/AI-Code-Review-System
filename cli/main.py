import typer
from rich import print

from cli.git_utils import get_changed_files
from cli.diff_parser import extract_diff_context
from cli.chunker import chunk_code
from cli.prompt_builder import build_prompt
from cli.client import send_for_review


def review(path: str = "."):
    """Run AI code review on a repository."""

    print("[bold green]Starting AI Code Review[/bold green]")

    files = get_changed_files(path)

    if not files:
        print("No changed files detected.")
        return

    for file_path, content in files:

        print(f"\n[cyan]Reviewing file:[/cyan] {file_path}")

        diff_context = extract_diff_context(file_path)

        chunks = chunk_code(diff_context)

        for i, chunk in enumerate(chunks):

            print(f"Processing chunk {i+1}/{len(chunks)}")

            prompt = build_prompt(file_path, chunk)

            result = send_for_review(prompt)

            print(result)


if __name__ == "__main__":
    typer.run(review)