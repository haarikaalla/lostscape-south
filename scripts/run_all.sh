#!/usr/bin/env bash
set -euo pipefail
export MPLBACKEND=Agg
export MPLCONFIGDIR="${PWD}/work/mplcache"
export XDG_CACHE_HOME="${PWD}/work/cache"
mkdir -p "$MPLCONFIGDIR" "$XDG_CACHE_HOME"
if [[ -x .venv/bin/python ]]; then PYTHON_BIN=.venv/bin/python; elif command -v python3 >/dev/null; then PYTHON_BIN=python3; else PYTHON_BIN=python; fi
"$PYTHON_BIN" -m src.data.build_inventory
if [[ -f data/private/features_5km_karnataka.csv && -f data/private/master_inventory_precise.csv ]]; then
  "$PYTHON_BIN" -m src.data.prepare_training
  "$PYTHON_BIN" -m src.models.baselines
  "$PYTHON_BIN" -m src.models.experiments
  "$PYTHON_BIN" -m src.eval.phase5
  "$PYTHON_BIN" -m src.risk.phase6
  "$PYTHON_BIN" -m src.history.hampi_case
  "$PYTHON_BIN" -m src.history.lost_settlement_tests
  "$PYTHON_BIN" -m src.eval.pseudo_discovery
  if compgen -G 'data/private/landsat_history_*.csv' >/dev/null; then "$PYTHON_BIN" -m src.history.analyse_landsat_pilots; fi
  "$PYTHON_BIN" -m src.survey.blind_spots
  if [[ -f data/private/site_damage_history_2016_2025.csv ]]; then "$PYTHON_BIN" -m src.risk.site_damage_forecast; fi
  if [[ -f results/tables/site_damage_forecast_cells.csv ]]; then "$PYTHON_BIN" -m src.eval.candidate_outcomes; fi
  "$PYTHON_BIN" -m src.eval.headline_atlas
else
  echo "Private feature inputs absent: reproducibly skipping model stages. See docs/DATA_SOURCES.md."
fi
"$PYTHON_BIN" scripts/privacy_scan.py
"$PYTHON_BIN" -m pytest -q
echo "Local reproducible stages complete. Earth Engine exports remain separately resumable."

