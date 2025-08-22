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
# Files that indicate a directory is a virtual environment
VENV_INDICATORS = [
    'pyvenv.cfg',                   # Python 3.3+ venv
    'bin/activate',                 # Unix virtualenv/venv
    'Scripts/activate.bat',         # Windows virtualenv/venv
    'Scripts/activate.ps1',         # PowerShell activation
    'pip-selfcheck.json',           # Common in virtualenvs
    'lib/'                          # Virtualenv library directory
]

# Directory names that are likely virtual environments
DEFAULT_VENV_NAMES = ['venv', '.venv', 'env']  # Removed '.env' to avoid false positives

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

# File and directory suffixes to delete (e.g., foo.egg-info or foo.egg-info/)
SUFFIXES_TO_DELETE = ['.egg-info']


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
    """Check if a directory is a virtual environment.
    
    A directory is considered a virtual environment if:
    1. It has a standard venv name AND contains at least one venv indicator file, or
    2. It contains multiple indicator files suggesting it's a virtual environment
    """
    path = os.path.abspath(path)
    dir_name = os.path.basename(path)
    
    # Check for standard venv names first
    if dir_name in DEFAULT_VENV_NAMES:
        # For standard names, require at least one indicator file
        for indicator in VENV_INDICATORS:
            if os.path.exists(os.path.join(path, indicator)):
                return True
        return False
    
    # For non-standard names, require multiple indicators to confirm it's a venv
    indicator_count = 0
    for indicator in VENV_INDICATORS:
        if os.path.exists(os.path.join(path, indicator)):
            indicator_count += 1
            # If we find multiple indicators, it's likely a venv
            if indicator_count > 1:
                return True
    
    return False


def discover_targets(root_dir, recursive=False):
    """Scan the directory tree and identify items to be deleted.
    
    Returns:
        list: A list of tuples containing (path, kind, size) for each item to delete.
             kind can be 'dir', 'file', or 'venv'.
    """
    targets = []
    
    # Using list(dirnames) creates a copy that we can safely iterate over while modifying dirnames
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=True):
        # Check directories (virtual envs and cache dirs)
        for d in list(dirnames):  # Create a copy to safely modify dirnames during iteration
            full_path = os.path.join(dirpath, d)
            if is_venv(full_path):
                kind = 'venv'
            elif d in DIRECTORIES_TO_DELETE:
                kind = 'dir'
            else:
                continue
                
            size = get_dir_size(full_path)
            targets.append((full_path, kind, size))
            dirnames.remove(d)  # Prevent further processing of this directory
        
        # Check files and directories with deletable suffixes
        for item in list(filenames) + list(dirnames):
            full_path = os.path.join(dirpath, item)
            is_dir = item in dirnames
            
            # Skip if no matching suffix
            if not any(item.endswith(suffix) for suffix in SUFFIXES_TO_DELETE):
                continue
                
            try:
                size = get_dir_size(full_path) if is_dir else os.path.getsize(full_path)
                targets.append((full_path, 'dir' if is_dir else 'file', size))
                if is_dir:
                    dirnames.remove(item)  # Prevent further processing of this directory
            except OSError:
                continue
                
        if not recursive:
            dirnames.clear()  # Clear to prevent descending into subdirectories
            
    return targets


def execute_cleanup(targets, dry_run=False):
    """Execute the actual cleanup operation on discovered targets.
    
    Args:
        targets: List of (path, kind, size) tuples from discover_targets()
        dry_run: If True, only log what would be deleted
        
    Returns:
        tuple: (deleted_items, total_size, logs)
    """
    deleted_items = []
    total_size = 0
    logs = []
    
    for path, kind, size in targets:
        # Determine icon and description based on item type
        if kind == 'venv':
            icon = "📦"
            desc = os.path.basename(path)
        elif kind == 'dir':
            icon = "📂"
            desc = os.path.basename(path)
        else:  # file
            icon = "📄"
            desc = os.path.basename(path)
            
        logs.append(f"{icon} {desc:20} {human_readable_size(size)}")
        
        if not dry_run:
            try:
                if kind in ('venv', 'dir'):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
                deleted_items.append((path, size))
                total_size += size
            except OSError as e:
                logs.append(f"⚠️ Error deleting {path}: {e}")
        else:
            deleted_items.append((path, size))
            total_size += size
            
    return deleted_items, total_size, logs


def find_and_delete(root_dir, dry_run=False, recursive=False):
    """Find and delete specified directories, files, and virtual environments."""
    # Phase 1: Discover all targets
    targets = discover_targets(root_dir, recursive)
    
    # Phase 2: Execute cleanup on all targets
    return execute_cleanup(targets, dry_run)


class Spinner:
    """A simple spinner animation that can be toggled and won't interfere with logs."""
    
    def __init__(self, enabled=True):
        self.enabled = enabled
        self.stop_event = threading.Event()
        self.thread = None
        self.last_line_length = 0
    
    def _clear_line(self):
        """Clear the current line by overwriting with spaces."""
        if self.enabled and self.last_line_length > 0:
            sys.stdout.write("\r" + " " * (self.last_line_length + 1) + "\r")
            sys.stdout.flush()
            self.last_line_length = 0
    
    def _spinner_loop(self):
        """Internal spinner animation loop."""
        frames = ["🧹", "🧹", "🧹.", "🧹..", "🧹..."]
        while not self.stop_event.is_set():
            for frame in frames:
                if self.stop_event.is_set():
                    break
                self._clear_line()
                msg = f"Sweeping project... {frame}"
                sys.stdout.write(f"\r{msg}")
                sys.stdout.flush()
                self.last_line_length = len(msg)
                time.sleep(0.2)
    
    def start(self):
        """Start the spinner animation in a separate thread if enabled."""
        if not self.enabled:
            return
            
        self.stop_event.clear()
        self.thread = threading.Thread(target=self._spinner_loop)
        self.thread.daemon = True
        self.thread.start()
    
    def stop(self, message="Done sweeping! 🧹"):
        """Stop the spinner and display a completion message."""
        if not self.enabled:
            return
            
        self.stop_event.set()
        if self.thread:
            self.thread.join(timeout=0.5)
        self._clear_line()
        if message:
            print(f"\r{message}")
        sys.stdout.flush()


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
    parser.add_argument(
        '--spinner',
        action='store_true',
        help="Show a spinner animation during the cleanup (default: off)."
    )
    args = parser.parse_args()

    start_path = os.path.abspath(args.path)
    print(f"Starting cleanup in: {start_path} ({'recursive' if args.recursive else 'top-level only'})\n")

    # Initialize and start the spinner if enabled
    spinner = Spinner(enabled=args.spinner)
    spinner.start()

    try:
        # Run cleanup
        deleted, total_size, logs = find_and_delete(start_path, args.dry_run, args.recursive)
        
        # Stop spinner before printing results
        spinner.stop()
        
        # Print results
        if logs:
            print("\n--- Detected Items ---" if not args.dry_run else "\n--- Detected Items (dry run) ---")
            for line in logs:
                print(line)

        if deleted:
            action = "Would delete" if args.dry_run else "Deleted"
            print("\n--- Summary ---")
            print(f"{action} {len(deleted)} item{'s' if len(deleted)!=1 else ''}, "
                  f"total size {human_readable_size(total_size)}")
        else:
            print("\nNo matching directories or files found to delete.")
            
    except Exception as e:
        # Ensure spinner is stopped on error
        spinner.stop(f"Error during cleanup: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
