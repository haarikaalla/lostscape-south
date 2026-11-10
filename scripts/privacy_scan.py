"""Fail before release when tracked files expose sensitive data or secrets."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PROHIBITED=("data/private/","data/raw/")
ALLOWED_RAW_SUFFIXES=(".txt",".sparql",".gitkeep")
SECRET_PATTERNS={
    "GitHub token":re.compile(r"gh[oprsu]_[A-Za-z0-9_]{20,}"),
    "Google API key":re.compile(r"AIza[0-9A-Za-z_-]{30,}"),
    "Private key":re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}
COORDINATE_PAIR=re.compile(r"(?<![\w.])-?\d{1,2}\.\d{4,}\s*[,; ]\s*-?\d{2,3}\.\d{4,}(?![\w.])")


def main() -> None:
    files=subprocess.check_output(["git","ls-files"],cwd=ROOT,text=True).splitlines(); problems=[]
    for rel in files:
        path=ROOT/rel
        if rel.startswith("data/private/") and not rel.endswith(".gitkeep"): problems.append(f"private path tracked: {rel}")
        if rel.startswith("data/raw/") and not rel.endswith(ALLOWED_RAW_SUFFIXES): problems.append(f"raw download tracked: {rel}")
        if path.stat().st_size>10*1024*1024: problems.append(f"file exceeds 10 MiB: {rel}")
        if path.suffix.lower() in {".png",".pdf",".svg"}: continue
        text=path.read_text(errors="ignore")
        for name,pattern in SECRET_PATTERNS.items():
            if pattern.search(text): problems.append(f"{name} pattern: {rel}")
        if rel.startswith(("data/processed/","results/")) and COORDINATE_PAIR.search(text): problems.append(f"possible precise coordinate pair: {rel}")
    if problems:
        print("PRIVACY SCAN FAILED")
        print("\n".join(f"- {p}" for p in problems))
        raise SystemExit(1)
    print(f"PRIVACY SCAN PASSED: {len(files)} tracked files checked")


if __name__=="__main__": main()
