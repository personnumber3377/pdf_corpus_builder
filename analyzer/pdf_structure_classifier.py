#!/usr/bin/env python3
"""
Classifies PDFs by structural uniqueness based on pikepdf object keys.
Moves unique PDFs to ./data/accepted
Others → ./data/rejected
"""

import json, hashlib, shutil
from pathlib import Path
import pikepdf

QUEUE = Path("data/queue/")
ACCEPT = Path("data/accepted/")
REJECT = Path("data/rejected/")
SIGFILE = Path("data/signatures.json")

ACCEPT.mkdir(parents=True, exist_ok=True)
REJECT.mkdir(parents=True, exist_ok=True)

if SIGFILE.exists():
    signatures = set(json.loads(SIGFILE.read_text()))
else:
    signatures = set()


def pdf_signature(path):
    try:
        pdf = pikepdf.Pdf.open(path)
    except:
        return None

    keys = []

    # Only inspect first 60 objects to keep things fast
    for obj in list(pdf.objects)[:60]:
        if hasattr(obj, "keys"):
            keys.extend(list(obj.keys()))

    # Normalize
    keys = sorted(set(keys))
    digest = hashlib.sha1(" ".join(keys).encode()).hexdigest()
    return digest


def main():
    for pdf in QUEUE.iterdir():
        if not pdf.name.endswith(".pdf"):
            continue

        sig = pdf_signature(pdf)

        if sig is None:
            print("BAD PDF", pdf)
            (REJECT / pdf.name).write_bytes(pdf.read_bytes())
            pdf.unlink()
            continue

        if sig not in signatures:
            print("[+] NEW STRUCTURE", pdf)
            signatures.add(sig)
            shutil.move(str(pdf), ACCEPT / pdf.name)
        else:
            print("[x] DUPLICATE STRUCTURE", pdf)
            shutil.move(str(pdf), REJECT / pdf.name)

    SIGFILE.write_text(json.dumps(list(signatures), indent=2))

if __name__ == "__main__":
    main()