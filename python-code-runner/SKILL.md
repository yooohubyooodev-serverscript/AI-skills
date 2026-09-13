---
name: python-code-runner
description: Execute Python code safely and capture results. Use when the user asks to run Python, test code snippets, compute values, debug scripts, or verify program behavior. Triggers include run this code, execute python, test this snippet, calculate with python, verify output.
---

# Python Code Runner

## Overview

Run arbitrary Python code in a controlled way, capture stdout/stderr, handle timeouts and errors, and return structured results. Prefer this over guessing execution outcomes.

## When to Use

- User provides Python code and asks to run, test, or see the output
- Need to verify correctness of a snippet
- Perform calculations, data processing, or quick experiments that require real execution
- Debug by running and inspecting errors

## Instructions

1. **Prepare the code**
   - Write the user's code (or a minimal repro) into a temporary `.py` file under `/tmp` or the working directory.
   - If the code needs input data or files, place them alongside the script.
   - Prefer pure standard-library code. If third-party packages are required, check availability first with `python -c "import package"`.

2. **Execute safely**
   - Always use a timeout (default 30 seconds).
   - Capture both stdout and stderr.
   - Prefer the helper script `scripts/run_python.py` when available:
     ```
     python scripts/run_python.py --timeout 30 --file /tmp/snippet.py
     ```
     or pipe code via stdin:
     ```
     echo 'print(1+1)' | python scripts/run_python.py --timeout 10
     ```
   - Fallback command if helper is missing:
     ```
     timeout 30s python /tmp/snippet.py 2>&1
     ```

3. **Handle results**
   - Report exit code, stdout, and stderr clearly.
   - If the process timed out, say so and show partial output if any.
   - If ImportError or missing dependency occurs, list the missing package and ask whether to install (only if the environment allows `pip install`).
   - Never execute code that attempts network access, file system writes outside the working/tmp area, or subprocess calls that could be dangerous unless the user explicitly requests it and the environment is known to be sandboxed.

4. **Best practices**
   - Keep snippets self-contained.
   - Add `if __name__ == "__main__":` guards when the code is a module.
   - For interactive or multi-step sessions, reuse the same temporary directory.
   - Clean up temporary files after reporting results unless the user wants to keep them.

5. **Security notes**
   - Treat all user-supplied code as untrusted.
   - Do not run code that reads environment variables containing secrets, opens arbitrary network sockets, or modifies system state.
   - Prefer read-only operations.

## Helper Script

The script `scripts/run_python.py` provides a consistent interface for execution. Read it when you need the exact flags or behavior.
