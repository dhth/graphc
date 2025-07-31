import os
import subprocess
from pathlib import Path
from typing import Callable

import pytest

Runner = Callable[[list[str], dict[str, str]], str]


@pytest.fixture
def runner() -> Runner:
    project_root = Path(__file__).parent.parent

    def _run(args: list[str], env: dict[str, str]) -> str:
        cmd = ["uv", "run", "src/main.py"] + args

        process_env = os.environ.copy()
        process_env.update(env)

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=project_root,
            env=process_env,
        )

        success = result.returncode == 0

        output = f"success: {str(success).lower()}\n"
        output += f"exit_code: {result.returncode}\n"
        output += "----- stdout -----\n"
        output += result.stdout
        if not result.stdout.endswith("\n"):
            output += "\n"
        output += "----- stderr -----\n"
        output += result.stderr
        if result.stderr and not result.stderr.endswith("\n"):
            output += "\n"

        return output

    return _run
