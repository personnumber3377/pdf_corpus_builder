#!/usr/bin/env python3
"""
Collects PDF URLs from known testsets + web crawling.
Stores URLs in ./data/url_queue.txt
"""

import re, requests, time, os
from urllib.parse import urljoin, urlparse
from pathlib import Path

OUTPUT = Path("data/url_queue.txt")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

SEEDS = [
    "https://www.pdfa.org/resources/",
    "https://corpora.uni-leipzig.de/",
    "https://github.com/pdf-association",
    "https://github.com/mozilla/pdf.js/tree/master/test/pdfs",
    "https://samples.libreoffice.org/",
    "https://github.com/gotenberg/gotenberg",
    "https://github.com/veraPDF/veraPDF-corpus",
]

SEEN = set()

def extract_pdfs(url):
    try:
        r = requests.get(url, timeout=10)
    except:
        return []

    links = re.findall(r'href=["\'](.*?)["\']', r.text)
    results = []

    for link in links:
        full = urljoin(url, link)
        if full.lower().endswith(".pdf") and full not in SEEN:
            SEEN.add(full)
            results.append(full)

    return results


def main():
    with open(OUTPUT, "a") as f:
        for seed in SEEDS:
            print(f"[+] Crawling {seed}")
            urls = extract_pdfs(seed)
            for u in urls:
                print(" ->", u)
                f.write(u + "\n")
            time.sleep(1)

    print("[DONE] URLs saved to", OUTPUT)

if __name__ == "__main__":
    main()