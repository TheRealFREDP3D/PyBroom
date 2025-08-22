# 🧹 PyBroom

**PyBroom** is a simple Python CLI tool that sweeps away common project clutter:  
virtual environments, `__pycache__` directories, build artifacts, and more.  
Think of it like `cargo clean` for Python projects.

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

Example output:
```
🧹 PyBroom - Sweep away Python clutter

Starting cleanup in: ./myproject (recursive)

Sweeping project... 🧹
Done sweeping! 🧹   

--- Detected Items (dry run) ---
📦 .venv                 524.98 KB
🗂️ __pycache__           45.12 KB
📄 mypkg.egg-info        2.10 KB

--- Summary ---
Would delete 3 items, total size 572.20 KB
```

---

## 📦 Roadmap
- [ ] Config file (`.pybroom.json`) for custom cleanup patterns.
- [ ] Exclusion patterns (e.g., `--exclude node_modules`).
- [ ] Colored output with `rich`.
- [ ] Git hook integration (auto-clean before commit).

---

## Contributing
Contributions are welcome!  
Open an issue or PR to suggest improvements.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Made with by Frederick Pellerin 2025 Frederick Pellerin
