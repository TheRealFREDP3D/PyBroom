# PyBroom 🧹

Sweep away Python clutter!  
Removes `__pycache__` folders and Python virtual environments with a single command.

## 1. Installation

```bash
pip install .
```

---

## 2. Usage

Do a dry run to see code execution without removing files

```sh
pybroom --path /my/project --dry-run
```

Execute script and delete Python cache and virtual environment files

```sh
pybroom --path /my/project
```

## 3. clean2.py details

Purpose
- Recursively scans a starting directory and:
  - Detects and deletes Python virtual environments (names like `venv`, `.venv`, `env`, `.env`, or folders containing indicators like `pyvenv.cfg`, `bin/activate`, `Scripts/activate.bat`).
  - Deletes Python cache directories named `__pycache__`.
- Supports a dry-run mode to preview what would be deleted.

How it works
- Prints a small ASCII banner at start.
- Identifies virtual environments by folder name or by common venv indicators.
- Walks the directory tree top-down; when a target directory is found, it is deleted (or listed in dry-run) and skipped from further traversal.
- Errors during deletion are caught and printed.

Examples
- Preview from the current directory:
  - `python clean2.py --dry-run`
- Actually delete from the current directory:
  - `python clean2.py`
- Target a specific folder:
  - `python clean2.py --path "/path/to/project"`

Customization
- Adjust what counts as a venv via `DEFAULT_VENV_NAMES` and `VENV_INDICATORS`.
- Add more cache directories to delete by editing `DIRECTORIES_TO_DELETE` (e.g., add `.pytest_cache`, `.mypy_cache`).

## 4. Author

**Frederick Pellerin**

|-----				  						|
|Mail     	fredp3d@proton.me 				|
|[X](https://x.com/therealfredp3d)		|
|[Github](https://github.com/therealfredp3d)	|
|[Website](https://therealfred.ca)				|
