#!/usr/bin/env python3
"""Verify that published GitHub Pages files exactly match the checked-out main tree.

Fail closed: a successful commit/PR or a Pages HTTP 200 is not enough.
This is machine byte-level QA; real devices and human PDF review remain separate.
"""
from __future__ import annotations
import hashlib
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://aipmandy.github.io/one-person-ai-income-guide/"
PATHS = [
    "index.html", "cashflow.html", "assets/cashflow.js",
    "robots.txt", "sitemap.xml", "pdf/one-person-ai-income-guide-guide.pdf",
]

def check_once() -> list[str]:
    errors = []
    for path in PATHS:
        expected = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
        url = BASE + ("" if path == "index.html" else path)
        req = urllib.request.Request(url, headers={
            "User-Agent": "aipmandy-site-verifier/1.0",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        })
        try:
            with urllib.request.urlopen(req, timeout=18) as response:
                actual = hashlib.sha256(response.read()).hexdigest()
                if response.status != 200 or actual != expected:
                    errors.append(f"{path}: HTTP {response.status}, sha256 {actual} != {expected}")
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            errors.append(f"{path}: {type(exc).__name__}: {exc}")
    return errors

def main():
    for n in range(1, 25):
        errors = check_once()
        if not errors:
            print(f"PASS: {len(PATHS)}/{len(PATHS)} public files HTTP 200 and SHA-256 equal to main.")
            for path in PATHS:
                print(BASE + ("" if path == "index.html" else path))
            return 0
        print(f"Attempt {n}/24: {len(errors)} live mismatches", flush=True)
        for error in errors:
            print("  " + error, flush=True)
        if n < 24:
            time.sleep(20)
    print("FAIL: Deployment could not be proven by public byte matching.", file=sys.stderr)
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
