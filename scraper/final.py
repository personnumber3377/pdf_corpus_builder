#!/usr/bin/env python3
import requests, os, re, hashlib, time
from pathlib import Path
from urllib.parse import urljoin

OUT = Path("download_queue.txt")
# OUT.mkdir(parents=True, exist_ok=True)

SOURCES = [
    "https://github.com/mozilla/pdf.js/tree/master/test/pdfs",
    "https://github.com/veraPDF/veraPDF-corpus/tree/master",
    "https://github.com/madler/zlib/tree/master/contrib/testpdf",
    "https://github.com/ArtifexSoftware/ghostpdl/tree/master/gs/toolbin/tests",
    "https://github.com/pdf-association/pdfa-testsuite/tree/master",
    "https://github.com/google/pdfium/tree/main/testing/resources",
]

def extract_pdf_links(url):
    print("Scanning:", url)
    r = requests.get(url)
    links = set(re.findall(r'href="([^"]+\.pdf)"', r.text))

    with open("download_queue.txt", "a+") as f:
        for link in links:
            full = urljoin(url, link)
            f.write(full + "\n")
            print("Found PDF:", full)

for s in SOURCES:
    extract_pdf_links(s)
    # time.sleep(1)