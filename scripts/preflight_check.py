#!/usr/bin/env python3

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path


REQUIRED_COMMANDS = [
    "python",
    "uvicorn",
    "jq",
    "ngrok",
    "nc",
    "ruff",
    "bandit",
    "semgrep",
]

REQUIRED_ENV_VARS = [
    "GITHUB_TOKEN",
    "GITHUB_REPO",
    "WEBHOOK_ID",
    "NGROK_AUTH_TOKEN",
]


def parse_env_file(env_path: Path) -> dict[str, str]:
    if not env_path.exists():
        return {}

    values: dict[str, str] = {}
    for raw_line in env_path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, val = line.split("=", 1)
        values[key.strip()] = val.strip().strip('"').strip("'")

    return values


def resolve_env(var_name: str, env_file_values: dict[str, str]) -> str | None:
    if os.getenv(var_name):
        return os.getenv(var_name)
    return env_file_values.get(var_name)


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    env_path = project_root / ".env"
    env_file_values = parse_env_file(env_path)

    missing_commands = [cmd for cmd in REQUIRED_COMMANDS if shutil.which(cmd) is None]

    missing_env_vars = [
        var for var in REQUIRED_ENV_VARS if not resolve_env(var, env_file_values)
    ]

    if missing_commands or missing_env_vars:
        print("❌ Preflight failed")

        if missing_commands:
            print("\nMissing required commands:")
            for cmd in missing_commands:
                print(f"  - {cmd}")

        if missing_env_vars:
            print("\nMissing required environment variables:")
            for var in missing_env_vars:
                print(f"  - {var}")

        print("\nHow to fix:")
        print("  1. Install missing binaries and ensure they are on PATH.")
        print("  2. Create .env from .env.example and fill required values.")
        print("  3. Re-run: make preflight")
        return 1

    print("✅ Preflight passed")
    print("All required binaries and environment variables are configured.")
    return 0


if __name__ == "__main__":
    sys.exit(main())