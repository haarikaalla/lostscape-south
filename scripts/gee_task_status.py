"""Report Earth Engine task states as JSON."""
import json
from pathlib import Path
import ee, yaml

ROOT=Path(__file__).resolve().parents[1]
cfg=yaml.safe_load((ROOT/"config.yaml").read_text()); ee.Initialize(project=cfg["gee"]["project"])
print(json.dumps([t.status() for t in ee.batch.Task.list()],indent=2))
