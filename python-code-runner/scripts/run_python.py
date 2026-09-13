#!/usr/bin/env python3
"""
Safe-ish Python code runner for AI agents.
Supports file or stdin input, timeout, and structured output.
"""

import argparse
import subprocess
import sys
import tempfile
import os
from pathlib import Path


def run_code(code: str | None = None, file_path: str | None = None, timeout: float = 30.0) -> dict:
    """Execute Python code and return structured result."""
    if code is None and file_path is None:
        return {"ok": False, "error": "No code or file provided"}

    tmp_file = None
    try:
        if file_path:
            script = Path(file_path)
            if not script.exists():
                return {"ok": False, "error": f"File not found: {file_path}"}
            cmd = [sys.executable, str(script)]
        else:
            # Write code to a temporary file for cleaner traceback paths
            fd, tmp_path = tempfile.mkstemp(suffix=".py", prefix="ai_run_")
            os.close(fd)
            tmp_file = Path(tmp_path)
            tmp_file.write_text(code, encoding="utf-8")
            cmd = [sys.executable, str(tmp_file)]

        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            env={**os.environ, "PYTHONUNBUFFERED": "1"},
        )

        return {
            "ok": proc.returncode == 0,
            "returncode": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "timeout": False,
        }
    except subprocess.TimeoutExpired as e:
        return {
            "ok": False,
            "returncode": -1,
            "stdout": e.stdout or "",
            "stderr": (e.stderr or "") + f"\n[TIMEOUT after {timeout}s]",
            "timeout": True,
        }
    except Exception as e:
        return {
            "ok": False,
            "error": str(e),
            "returncode": -2,
            "stdout": "",
            "stderr": "",
            "timeout": False,
        }
    finally:
        if tmp_file and tmp_file.exists():
            try:
                tmp_file.unlink()
            except OSError:
                pass


def main():
    parser = argparse.ArgumentParser(description="Run Python code with timeout and capture")
    parser.add_argument("--file", "-f", help="Path to .py file")
    parser.add_argument("--timeout", "-t", type=float, default=30.0, help="Timeout in seconds")
    parser.add_argument("--json", action="store_true", help="Output result as JSON")
    args = parser.parse_args()

    code = None
    if not args.file and not sys.stdin.isatty():
        code = sys.stdin.read()

    result = run_code(code=code, file_path=args.file, timeout=args.timeout)

    if args.json:
        import json
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if result.get("stdout"):
            print(result["stdout"], end="")
        if result.get("stderr"):
            print(result["stderr"], file=sys.stderr, end="")
        if result.get("error"):
            print(f"[ERROR] {result['error']}", file=sys.stderr)
        sys.exit(result.get("returncode", 1) if not result.get("ok") else 0)


if __name__ == "__main__":
    main()
