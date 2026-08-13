# monitor.py
# File integrity monitor using SHA256 cryptographic hashing

import datetime
import hashlib
import json
import os

BASELINE_FILE = "baseline.json"
TARGET_DIR = "." # monitor current directory; change as needed

def hash_file(filepath):
    sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    except OSError:
        return None

def scan_directory(directory):
    hashes = {}
    for root, dirs, files in os.walk(directory):
        ignore_dirs = ["venv", "errors_screenshots", "__pycache__"]
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for name in files:
            path = os.path.join(root, name)
            if name == BASELINE_FILE:
                continue
            file_hash = hash_file(path)
            if file_hash:
                hashes[path] = file_hash
    return hashes

def create_baseline():
    baseline = scan_directory(TARGET_DIR)
    with open(BASELINE_FILE, "w") as f:
        json.dump(baseline, f, indent=4)
    print(f"Baseline created with {len(baseline)} files.")

def check_integrity():
    if not os.path.exists(BASELINE_FILE):
        print("No baseline found. Create one first.")
        return

    with open(BASELINE_FILE, "r") as f:
        old = json.load(f)

    current = scan_directory(TARGET_DIR)
    old_files = set(old.keys())
    current_files = set(current.keys())

    added = current_files - old_files
    deleted = old_files - current_files
    common = old_files & current_files
    modified = [path for path in common if old[path] != current[path]]

    print(f"Integrity check: {datetime.datetime.now()}")
    for path in added:
        print(f"ADDED: {path}")
    for path in deleted:
        print(f"DELETED: {path}")
    for path in modified:
        print(f"MODIFIED: {path}")

    if not added and not deleted and not modified:
        print("No changes detected.")

choice = input("Create baseline or check integrity? (create/check): ").lower().strip()
if choice == "create":
    create_baseline()
elif choice == "check":
    check_integrity()
else:
    print("Please choose create or check.")
