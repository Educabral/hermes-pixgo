# Python Paths on This Windows Setup (Git Bash / MSYS2)

## The Problem

`python3` in git-bash points to the WindowsApps directory, which redirects to the Microsoft Store — it fails silently or opens the Store instead of running Python.

```
$ which python3
/c/Users/PC/AppData/Local/Microsoft/WindowsApps/python3

$ which python
/c/Users/PC/AppData/Local/hermes/hermes-agent/venv/Scripts/python
```

## Working Python Paths

| Source | Path |
|--------|------|
| System Python 3.11 | `C:/Users/PC/AppData/Local/Programs/Python/Python311/python.exe` |
| Hermes venv Python | `/c/Users/PC/AppData/Local/hermes/hermes-agent/venv/Scripts/python` |
| pip/system packages | Installed to the system Python 3.11 (`pip install`) |

## Best Practice

When writing Python scripts in terminal() calls:

- **Use the hermetic venv Python** for scripts that use Hermes tools (it has `hermes_tools`):
  ```
  /c/Users/PC/AppData/Local/hermes/hermes-agent/venv/Scripts/python -c "print('hello')"
  ```
  **This is the recommended default** — it has PIL/Pillow, requests, and most common packages.

- **Use the explicit system Python path** in background processes or when the venv Python doesn't have a specific package:
  ```
  "C:/Users/PC/AppData/Local/Programs/Python/Python311/python.exe" -c "print('hello')"
  ```

- **Never** rely on bare `python3` or `python` without checking which one resolves.

## Checking Available Python

```bash
which python3
which python
ls /c/Users/PC/AppData/Local/Programs/Python/
ls /c/Users/PC/AppData/Local/hermes/hermes-agent/venv/Scripts/python
```

## Packages Available (venv Python)

The Hermes venv Python typically has: PIL/Pillow, pytesseract, requests, pydantic, and common ML/data packages. Check with:
```bash
/c/Users/PC/AppData/Local/hermes/hermes-agent/venv/Scripts/python -m pip list
```
