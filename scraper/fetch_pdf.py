#!/usr/bin/env python3
"""
Downloads PDFs from url_queue into ./data/queue/
Enforces size limits
"""
import os, time, requests, hashlib
from pathlib import Path

MAX_SIZE = 150_000  # 150KB
QUEUE = Path("data/url_queue.txt")
OUT = Path("data/queue/")
OUT_REJECT = Path("data/rejected/")
OUT.mkdir(parents=True, exist_ok=True)
OUT_REJECT.mkdir(parents=True, exist_ok=True)

def filename_from_url(url):
    return hashlib.sha1(url.encode()).hexdigest() + ".pdf"

def download(url):
    try:
        r = requests.get(url, timeout=15)
    except:
        return None, "network error"

    if len(r.content) > MAX_SIZE:
        return None, f"too large: {len(r.content)}"

    return r.content, None

def main():
    lines = open(QUEUE).read().splitlines()
    for url in lines:
        fn = filename_from_url(url)
        outpath = OUT / fn

        if outpath.exists():
            print("SKIP exists", url)
            continue

        data, err = download(url)
        if err:
            print("REJECT", url, err)
            (OUT_REJECT / fn).write_text(err)
            continue

        outpath.write_bytes(data)
        print("[+] Saved", outpath)

        time.sleep(0.5)

if __name__ == "__main__":
    main()