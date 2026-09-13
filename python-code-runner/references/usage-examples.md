# Usage Examples

## Basic run via stdin

```bash
echo 'print(2 ** 10)' | python scripts/run_python.py
```

## Run a file with timeout

```bash
python scripts/run_python.py --file /tmp/my_script.py --timeout 10
```

## JSON output (for programmatic use)

```bash
echo 'print({"a": 1})' | python scripts/run_python.py --json
```

## Common patterns the agent should follow

1. Write user code to `/tmp/ai_snippet.py`
2. Run: `python /path/to/skill/scripts/run_python.py -f /tmp/ai_snippet.py -t 30`
3. Report stdout / stderr / returncode cleanly
4. Delete the temp file when done
