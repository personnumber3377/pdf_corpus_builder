#!/usr/bin/env python3
import requests, os, json, hashlib
from pathlib import Path

API_KEY = os.getenv("GOOGLE_API_KEY")
CX = os.getenv("GOOGLE_CX")

OUT = Path("data/url_queue.txt")
OUT.parent.mkdir(parents=True, exist_ok=True)

# QUERY = "filetype:pdf test suite pdf specification example sample fuzz earnings example test report pricing"
QUERY = "filetype:pdf test suite pdf specification example"
NUM = 10  # results per page, max 10

def search(query, start=1):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": CX,
        "q": query,
        "start": start,
    }
    r = requests.get(url, params=params).json()
    print(r)
    if "items" not in r:
        return []

    results = []
    for item in r["items"]:
        link = item.get("link", "")
        if link.lower().endswith(".pdf"):
            results.append(link)

    return results


MAX_PAGE = 10000

LIST_LEN = 1000

def main():
    with open(OUT, "a") as f:
        for start in list(range(1, MAX_PAGE, int(MAX_PAGE / LIST_LEN))):  # sorted(list(random.randrange(1, MAX_PAGE) for _ in range(LIST_LEN))) # [1, 11, 21, 31, 41]:
            results = search(QUERY, start)
            for link in results:
                print("Found:", link)
                f.write(link + "\n")

if __name__ == "__main__":
    main()