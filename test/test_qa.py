import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(".").parent.parent


def test_mypy():
    subprocess.run(
        [
            sys.executable,
            "-m",
            "mypy",
            REPO_ROOT / "dated.py",
            *(REPO_ROOT / "test").glob("**/*.py"),
        ]
    ).check_returncode()


def test_ruff():
    subprocess.run(
        [sys.executable, "-m", "ruff", "format", "--check"]
    ).check_returncode()
    subprocess.run([sys.executable, "-m", "ruff", "check"]).check_returncode()
