import subprocess
import sys
from pathlib import Path

import mypy.api

REPO_ROOT = Path(__file__).parent.parent


def test_mypy():
    stdout, stderr, returncode = mypy.api.run([str(REPO_ROOT)])
    sys.stdout.write(stdout)
    sys.stderr.write(stderr)
    assert returncode == 0


def test_ruff_format():
    subprocess.run(
        [sys.executable, "-m", "ruff", "format", "--check"],
        cwd=REPO_ROOT,
        check=True,
    )


def test_ruff_lint():
    subprocess.run(
        [sys.executable, "-m", "ruff", "check"],
        cwd=REPO_ROOT,
        check=True,
    )
