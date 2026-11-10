"""Join private Earth Engine grid features to known sites without publishing coordinates."""
from __future__ import annotations

from pathlib import Path
import glob

import numpy as np
import pandas as pd
import yaml
from sklearn.neighbors import BallTree

ROOT=Path(__file__).resolve().parents[2]


def main() -> None:
    cfg=yaml.safe_load((ROOT/"config.yaml").read_text())
    files=glob.glob(str(ROOT/"data/private/features_5km_*.csv"))
    if not files: raise FileNotFoundError("Download completed Earth Engine feature CSVs into data/private/ first")
    features=pd.concat([pd.read_csv(p).assign(feature_file=Path(p).name) for p in files],ignore_index=True)
    required={"latitude","longitude"}
    if not required.issubset(features): raise ValueError(f"Feature exports missing {sorted(required-features.columns)}")
    sites=pd.read_csv(ROOT/"data/private/master_inventory_precise.csv")
    positives=sites[sites["class"].eq("megalithic_burial")].dropna(subset=["lat","lon"])
    tree=BallTree(np.radians(positives[["lat","lon"]].to_numpy()),metric="haversine")
    distance,_=tree.query(np.radians(features[["latitude","longitude"]].to_numpy()),k=1)
    features["distance_to_known_megalith_km"]=distance[:,0]*6371.0088
    features["label_positive"]=(features.distance_to_known_megalith_km<=3.6).astype("int8")
    # Approximately 50 km spatial blocks; used only for grouping, never as a feature.
    features["block_y"]=(features.latitude*111.32//50).astype(int)
    features["block_x"]=(features.longitude*111.32*np.cos(np.radians(features.latitude))//50).astype(int)
    features["spatial_block"]=features.block_x.astype(str)+"_"+features.block_y.astype(str)
    out=ROOT/"data/private/model_table.csv"; features.to_csv(out,index=False)
    print(features.groupby("feature_file").label_positive.agg(["count","sum"]).to_string())


if __name__=="__main__": main()

