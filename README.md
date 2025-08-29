# 🧹 PyBroom

**PyBroom** is a simple Python CLI tool that sweeps away common project clutter:  
virtual environments, `__pycache__` directories, build artifacts, and more.  
Think of it like `cargo clean` for Python projects.

---

```bash
# Example output

███████████████████████████████████████████
█▄─▄▄─█▄─█─▄█▄─▄─▀█▄─▄▄▀█─▄▄─█─▄▄─█▄─▀█▀─▄█
██─▄▄▄██▄─▄███─▄─▀██─▄─▄█─██─█─██─██─█▄█─██
▀▄▄▄▀▀▀▀▄▄▄▀▀▄▄▄▄▀▀▄▄▀▄▄▀▄▄▄▄▀▄▄▄▄▀▄▄▄▀▄▄▄▀
 🧹🐍 PyBroom - Sweep away Python clutter 🧹🐍

Starting cleanup in: F:\BACKUO\PROJECTS (recursive)

Done sweeping! 🧹

--- Detected Items ---
✓ 📂 dist                 44.62 KB
✓ 📂 dist                 347.54 KB
✓ 📂 dist                 70.69 KB
✓ 📂 .pytest_cache        542.00 B
✓ 📂 __pycache__          155.00 B
✓ 📂 __pycache__          1.27 KB
[...snip...]
✓ 📂 __pycache__          14.91 KB
✓ 📂 __pycache__          158.00 B
✓ 📂 __pycache__          9.10 KB
✓ 📂 __pycache__          24.04 KB
✓ 📂 __pycache__          33.33 KB

--- Summary ---
Deleted 1121 items, total size 1.90 GB
```

---

## ✨ Features
- Detects and deletes:
  - Virtual environments (`venv`, `.venv`, `env`, `.env`, or detected by config files).
  - `__pycache__` folders.
  - Build/test artifacts:
    - `.pytest_cache`
    - `.mypy_cache`
    - `.ruff_cache`
    - `.tox`
    - `.hypothesis`
    - `build/` and `dist/`
    - `*.egg-info`
- **Dry-run mode** (`--dry-run`) to preview what would be deleted.
- **Recursive scan** (`--recursive`) or top-level only (default).
- **Disk usage summary**: reports how much space was reclaimed.
- **Fun broom animation** while sweeping 🧹

---

## 🚀 Installation

Clone and run directly:
```bash
git clone https://github.com/TheRealFREDP3D/PyBroom.git
cd PyBroom
python pybroom.py --help
```

Or install locally as a CLI:
```bash
pip install .
```

After install you can just run:
```bash
pybroom --help
```

---

## 🛠 Usage

```bash
# Show help
pybroom --help

# Clean only top-level clutter
pybroom --path .

# Clean recursively (subfolders too)
pybroom --path . --recursive

# Preview without deleting
pybroom --path . --recursive --dry-run
```

---

## Contributing
Contributions are welcome!  
Open an issue or PR to suggest improvements.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Made by Frederick Pellerin
