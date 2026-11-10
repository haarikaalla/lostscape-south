import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def test_privacy_scan_passes():
    subprocess.run([sys.executable,str(ROOT/"scripts/privacy_scan.py")],cwd=ROOT,check=True)


def test_private_data_not_tracked():
    tracked=subprocess.check_output(["git","ls-files"],cwd=ROOT,text=True).splitlines()
    assert not [p for p in tracked if p.startswith("data/private/") and not p.endswith(".gitkeep")]

