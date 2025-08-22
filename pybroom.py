# pybroom.py
import os
import shutil
import argparse
import threading
import itertools
import sys
import time

# --- ASCII broom banner ---
BROOM_ART = r"""
   _    _    
  (_\__/(,_
   \_/_   _\
   (_/   (_)   🧹 PyBroom - Sweep away Python clutter
"""

# --- Configuration ---
VENV_INDICATORS = ['pyvenv.cfg', 'bin/activate', 'Scripts/activate.bat']
DEFAULT_VENV_NAMES = ['venv', '.venv', 'env', '.env']

# Directories to delete
DIRECTORIES_TO_DELETE = [
    '__pycache__',
    '.pytest_cache',
    '.mypy_cache',
    '.ruff_cache',
    '.tox',
    '.hypothesis',
    'build',
    'dist'
]

# File suffixes to delete (e.g., foo.egg-info)
FILE_SUFFIXES_TO_DELETE = ['.egg-info']


def human_readable_size(size_bytes):
    """Convert bytes to a human-readable string."""
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = 0
    while size_bytes >= 1024 and i < len(size_name) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.2f} {size_name[i]}"


def get_dir_size(path):
    """Return total size of all files in a directory (in bytes)."""
    total = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                total += os.path.getsize(fp)
            except OSError:
                continue
    return total


def is_venv(path):
    """Check if a directory is a virtual environment."""
    if os.path.basename(os.path.abspath(path)) in DEFAULT_VENV_NAMES:
        return True
    for indicator in VENV_INDICATORS:
        if os.path.exists(os.path.join(path, indicator)):
            return True
    return False


def find_and_delete(root_dir, dry_run=False, recursive=False):
    """Find and delete specified directories, files, and virtual environments."""
    deleted_items = []
    total_size = 0
    logs = []  # For clean printing

    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=True):
        # Directories
        for d in list(dirnames):
            full_path = os.path.join(dirpath, d)
            if is_venv(full_path) or d in DIRECTORIES_TO_DELETE:
                size = get_dir_size(full_path)
                icon = "📦" if is_venv(full_path) else "🗂️"
                logs.append(f"{icon} {d:20} {human_readable_size(size)}")
                if not dry_run:
                    try:
                        shutil.rmtree(full_path)
                        deleted_items.append((full_path, size))
                        total_size += size
                    except OSError as e:
                        logs.append(f"⚠️ Error deleting {full_path}: {e}")
                else:
                    deleted_items.append((full_path, size))
                    total_size += size
                dirnames.remove(d)

        # Process files with deletable suffixes
        for f in list(filenames):
            full_path = os.path.join(dirpath, f)
            try:
                size = os.path.getsize(full_path)
                for suffix in FILE_SUFFIXES_TO_DELETE:
                    if f.endswith(suffix):
                        logs.append(f"📄 {f:20} {human_readable_size(size)}")
                        if not dry_run:
                            try:
                                os.remove(full_path)
                                deleted_items.append((full_path, size))
                                total_size += size
                            except OSError as e:
                                logs.append(f"⚠️ Error deleting {full_path}: {e}")
                        else:
                            deleted_items.append((full_path, size))
                            total_size += size
                        break
            except OSError:
                continue

        if not recursive:
            dirnames.clear()

    return deleted_items, total_size, logs


def spinner(stop_event):
    """Show a broom animation until stop_event is set."""
    for frame in itertools.cycle(["🧹", "🧹.", "🧹..", "🧹..."]):
        if stop_event.is_set():
            break
        sys.stdout.write(f"\rSweeping project... {frame} ")
        sys.stdout.flush()
        time.sleep(0.3)
    sys.stdout.write("\rDone sweeping! 🧹   \n")


def main():
    print(BROOM_ART)
    parser = argparse.ArgumentParser(
        description="🧹 Clean up Python project clutter: caches, virtual envs, build artifacts."
    )
    parser.add_argument(
        '--path',
        default='.',
        help='Starting directory to search from (default: current directory).'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help="List what would be deleted without actually deleting anything."
    )
    parser.add_argument(
        '--recursive',
        action='store_true',
        help="Recursively scan subdirectories (default: false)."
    )
    args = parser.parse_args()

    start_path = os.path.abspath(args.path)
    print(f"Starting cleanup in: {start_path} ({'recursive' if args.recursive else 'top-level only'})\n")

    # Start animation
    stop_event = threading.Event()
    t = threading.Thread(target=spinner, args=(stop_event,))
    t.start()

    # Run cleanup
    deleted, total_size, logs = find_and_delete(start_path, args.dry_run, args.recursive)

    # Stop animation
    stop_event.set()
    t.join()

    if logs:
        print("\n--- Detected Items ---" if not args.dry_run else "\n--- Detected Items (dry run) ---")
        for line in logs:
            print(line)

    if deleted:
        action = "Would delete" if args.dry_run else "Deleted"
        print("\n--- Summary ---")
        print(f"{action} {len(deleted)} item{'s' if len(deleted)!=1 else ''}, total size {human_readable_size(total_size)}")
    else:
        print("\nNo matching directories or files found to delete.")


if __name__ == "__main__":
    main()
