"""Coarse, resumable Earth Engine availability and clear-observation QA."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import ee
import geopandas as gpd
import pandas as pd
import yaml

ROOT=Path(__file__).resolve().parents[2]


def mask_s2(image: ee.Image) -> ee.Image:
    scl=image.select("SCL")
    clear=(scl.neq(3).And(scl.neq(8)).And(scl.neq(9)).And(scl.neq(10)).And(scl.neq(11)))
    return image.select("B4").updateMask(clear).copyProperties(image,["system:time_start"])


def ee_geometry(geom) -> ee.Geometry:
    return ee.Geometry(json.loads(gpd.GeoSeries([geom],crs=4326).to_json())["features"][0]["geometry"])


def collection_dates(collection: ee.ImageCollection) -> tuple[str|None,str|None,int]:
    count=int(collection.size().getInfo())
    if not count: return None,None,0
    lo=collection.aggregate_min("system:time_start").getInfo(); hi=collection.aggregate_max("system:time_start").getInfo()
    fmt=lambda x: datetime.fromtimestamp(x/1000,tz=timezone.utc).date().isoformat()
    return fmt(lo),fmt(hi),count


def main() -> None:
    cfg=yaml.safe_load((ROOT/"config.yaml").read_text()); project=cfg["gee"]["project"]
    ee.Initialize(project=project)
    borders=gpd.read_file(ROOT/"data/raw/boundaries_ind_adm1.geojson").to_crs(4326)
    borders["state_ascii"]=borders.shapeName.str.normalize("NFKD").str.encode("ascii",errors="ignore").str.decode("ascii")
    dates=("2017-03-28","2026-11-10"); rows=[]
    for state in cfg["region"]["states"]:
        geom=ee_geometry(borders.loc[borders.state_ascii.eq(state),"geometry"].iloc[0].simplify(0.01))
        base=ee.ImageCollection(cfg["gee"]["datasets"]["sentinel2"]).filterBounds(geom).filterDate(*dates)
        for season,start_month,end_month in [("dry",1,3),("post_monsoon",10,12),("all",1,12)]:
            coll=base.filter(ee.Filter.calendarRange(start_month,end_month,"month"))
            raw_count=coll.select("B4").count(); clear_count=coll.map(mask_s2).count()
            pct=clear_count.divide(raw_count.max(1)).multiply(100).rename("valid_pct")
            stats=pct.reduceRegion(ee.Reducer.mean(),geom,20000,bestEffort=True,maxPixels=250_000,tileScale=4).getInfo()
            n=int(coll.size().getInfo())
            rows.append({"state":state,"season":season,"dataset":cfg["gee"]["datasets"]["sentinel2"],"requested_start":dates[0],"requested_end":dates[1],"image_count":n,"mean_valid_observation_pct":stats.get("valid_pct")})
    out=ROOT/"results/tables"; out.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(rows).to_csv(out/"gee_observation_qa.csv",index=False)
    probes=[]
    for key,dataset in cfg["gee"]["datasets"].items():
        try: n=int(ee.ImageCollection(dataset).limit(1).size().getInfo())
        except Exception:
            image=ee.Image(dataset); n=1; image.bandNames().getInfo()
        probes.append({"key":key,"dataset_id":dataset,"availability_probe_count":n,"access_date":"2026-11-10"})
    pd.DataFrame(probes).to_csv(out/"gee_dataset_probe.csv",index=False)
    print(pd.DataFrame(rows).to_string(index=False))


if __name__=="__main__": main()
