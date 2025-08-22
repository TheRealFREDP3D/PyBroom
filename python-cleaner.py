# pybroom.py
import os
import shutil
import argparse

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
DIRECTORIES_TO_DELETE = ['__pycache__']


def is_venv(path):
    """Check if a directory is a virtual environment."""
    if os.path.basename(os.path.abspath(path)) in DEFAULT_VENV_NAMES:
        return True
    for indicator in VENV_INDICATORS:
        if os.path.exists(os.path.join(path, indicator)):
            return True
    return False


def find_and_delete(root_dir, dry_run=False):
    """Find and delete specified directories and virtual environments."""
    deleted_items = []
    for dirpath, dirnames, _ in os.walk(root_dir, topdown=True):
        for d in list(dirnames):
            full_path = os.path.join(dirpath, d)
            if is_venv(full_path):
                print(f"{'[DRY RUN] ' if dry_run else ''}Identified virtual environment: {full_path}")
                if not dry_run:
                    try:
                        shutil.rmtree(full_path)
                        deleted_items.append(full_path)
                    except OSError as e:
                        print(f"Error deleting {full_path}: {e}")
                else:
                    deleted_items.append(full_path)
                dirnames.remove(d)

        for d in list(dirnames):
            if d in DIRECTORIES_TO_DELETE:
                full_path = os.path.join(dirpath, d)
                print(f"{'[DRY RUN] ' if dry_run else ''}Identified cache directory: {full_path}")
                if not dry_run:
                    try:
                        shutil.rmtree(full_path)
                        deleted_items.append(full_path)
                    except OSError as e:
                        print(f"Error deleting {full_path}: {e}")
                else:
                    deleted_items.append(full_path)
                dirnames.remove(d)

    return deleted_items


def main():
    """Main CLI function."""
    print(BROOM_ART)
    parser = argparse.ArgumentParser(
        description="🧹 Recursively delete Python cache (__pycache__) and virtual environment directories."
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
    args = parser.parse_args()

    start_path = os.path.abspath(args.path)
    print(f"Starting cleanup in: {start_path}\n")

    deleted = find_and_delete(start_path, args.dry_run)

    if deleted:
        action = "Found and would delete" if args.dry_run else "Found and deleted"
        print("\n--- Summary ---")
        print(f"{action} {len(deleted)} item(s):")
        for item in deleted:
            print(f"- {item}")
    else:
        print("\nNo matching directories found to delete.")


if __name__ == "__main__":
    main()

