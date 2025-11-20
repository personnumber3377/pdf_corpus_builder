#!/usr/bin/env python3
"""
Select PDFs based on *new individual PDF object keys*.

A PDF is ACCEPTED if it contains ANY dictionary key that has not been
previously seen across all processed PDFs.

Tracks keys globally in data/keys_seen.json
Moves files accordingly:
    data/queue     -> input
    data/accepted  -> saved PDFs with new structure
    data/rejected  -> PDFs that add nothing new
"""

import json, hashlib, shutil
from pathlib import Path
import pikepdf

QUEUE = Path("data/queue/")
ACCEPT = Path("data/accepted/")
REJECT = Path("data/rejected/")
KEYFILE = Path("data/keys_seen.json")

ACCEPT.mkdir(parents=True, exist_ok=True)
REJECT.mkdir(parents=True, exist_ok=True)

# Load existing keys
if KEYFILE.exists():
    keys_seen = set(json.loads(KEYFILE.read_text()))
else:
    keys_seen = set()

MAX_OBJECTS = 200  # scan deeper than before


def extract_keys(path):
    """Return a set of all dictionary keys in the PDF."""
    try:
        pdf = pikepdf.Pdf.open(path)
    except Exception:
        return None

    newkeys = set()

    # Walk objects
    for obj in list(pdf.objects)[:MAX_OBJECTS]:
        if isinstance(obj, pikepdf.Dictionary):
            for key in obj.keys():
                if isinstance(key, pikepdf.Name):
                    newkeys.add(str(key))

        # Streams have dicts too
        if isinstance(obj, pikepdf.Stream):
            d = obj.get_dict()
            for key in d.keys():
                if isinstance(key, pikepdf.Name):
                    newkeys.add(str(key))

    return newkeys


def main():
    global keys_seen

    for pdf in QUEUE.iterdir():
        if not pdf.name.lower().endswith(".pdf"):
            continue

        keys = extract_keys(pdf)

        # Failed to read
        if keys is None:
            print("[-] Bad PDF:", pdf)
            shutil.move(str(pdf), REJECT / pdf.name)
            continue

        # Compare against global set
        new_keys = keys - keys_seen

        if new_keys:
            print(f"[+] NEW KEYS {pdf} :: {list(new_keys)[:10]}")
            keys_seen |= new_keys  # update global keyset
            shutil.move(str(pdf), ACCEPT / pdf.name)

        else:
            print(f"[x] NO NEW KEYS: {pdf}")
            shutil.move(str(pdf), REJECT / pdf.name)

        # Save updated key set after every PDF
        KEYFILE.write_text(json.dumps(sorted(list(keys_seen)), indent=2))


if __name__ == "__main__":
    main()