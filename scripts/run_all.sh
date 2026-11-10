#!/usr/bin/env bash
set -euo pipefail
python -m src.data.build_inventory
python scripts/privacy_scan.py
pytest -q
echo "Local reproducible stages complete. Earth Engine batch exports are managed separately."

