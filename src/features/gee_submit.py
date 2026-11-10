"""Submit resumable, state-tiled Earth Engine table exports."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import ee
import geopandas as gpd
import yaml

ROOT=Path(__file__).resolve().parents[2]


def geometry_for(state: str) -> ee.Geometry:
    borders=gpd.read_file(ROOT/"data/raw/boundaries_ind_adm1.geojson").to_crs(4326)
    names=borders.shapeName.str.normalize("NFKD").str.encode("ascii",errors="ignore").str.decode("ascii")
    geom=borders.loc[names.eq(state),"geometry"].iloc[0].simplify(0.005)
    return ee.Geometry(json.loads(gpd.GeoSeries([geom],crs=4326).to_json())["features"][0]["geometry"])


def mask_and_indices(image: ee.Image) -> ee.Image:
    scl=image.select("SCL")
    clear=scl.neq(3).And(scl.neq(8)).And(scl.neq(9)).And(scl.neq(10)).And(scl.neq(11))
    x=image.updateMask(clear).multiply(0.0001)
    ndvi=x.normalizedDifference(["B8","B4"]).rename("ndvi")
    ndwi=x.normalizedDifference(["B3","B8"]).rename("ndwi")
    evi=x.expression("2.5*((n-r)/(n+6*r-7.5*b+1))",{"n":x.select("B8"),"r":x.select("B4"),"b":x.select("B2")}).rename("evi")
    return x.select(["B2","B3","B4","B8"]).addBands([ndvi,ndwi,evi]).copyProperties(image,["system:time_start"])


def feature_stack(cfg: dict, geom: ee.Geometry) -> ee.Image:
    s2=ee.ImageCollection(cfg["gee"]["datasets"]["sentinel2"]).filterBounds(geom).filterDate("2017-03-28","2026-11-10").map(mask_and_indices)
    dry=s2.filter(ee.Filter.calendarRange(1,3,"month")); post=s2.filter(ee.Filter.calendarRange(10,12,"month"))
    dry_stats=dry.select(["ndvi","ndwi","evi"]).reduce(ee.Reducer.median().combine(ee.Reducer.stdDev(),sharedInputs=True)).rename(["dry_ndvi_med","dry_ndwi_med","dry_evi_med","dry_ndvi_sd","dry_ndwi_sd","dry_evi_sd"])
    post_stats=post.select(["ndvi","ndwi","evi"]).reduce(ee.Reducer.median().combine(ee.Reducer.stdDev(),sharedInputs=True)).rename(["post_ndvi_med","post_ndwi_med","post_evi_med","post_ndvi_sd","post_ndwi_sd","post_evi_sd"])
    valid=dry.select("ndvi").count().rename("dry_valid_n").addBands(post.select("ndvi").count().rename("post_valid_n"))
    s1=ee.ImageCollection(cfg["gee"]["datasets"]["sentinel1"]).filterBounds(geom).filterDate("2015-01-01","2026-11-10").filter(ee.Filter.eq("instrumentMode","IW")).filter(ee.Filter.listContains("transmitterReceiverPolarisation","VV")).filter(ee.Filter.listContains("transmitterReceiverPolarisation","VH")).select(["VV","VH"])
    sar=s1.reduce(ee.Reducer.median().combine(ee.Reducer.stdDev(),sharedInputs=True)).rename(["vv_med","vh_med","vv_sd","vh_sd"])
    dem=ee.Image(cfg["gee"]["datasets"]["dem"]).select("elevation").rename("elevation_m")
    terrain=ee.Terrain.products(dem).select(["slope","aspect"])
    rain=ee.ImageCollection(cfg["gee"]["datasets"]["rainfall"]).filterDate("2015-01-01","2026-01-01").select("precipitation").mean().rename("rain_daily_mean_mm")
    land=ee.ImageCollection(cfg["gee"]["datasets"]["worldcover"]).mosaic().select("Map").rename("worldcover")
    built=ee.ImageCollection(cfg["gee"]["datasets"]["dynamic_world"]).filterBounds(geom).filterDate("2015-01-01","2026-11-10").select("built").mean().rename("built_probability")
    return ee.Image.cat([dry_stats,post_stats,valid,sar,dem,terrain,rain,land,built,ee.Image.pixelLonLat()]).float()


def submit(cfg: dict) -> list[dict]:
    tasks=[]; states=cfg["region"]["states"]
    qa_features=[]
    for state in states:
        geom=geometry_for(state)
        base=ee.ImageCollection(cfg["gee"]["datasets"]["sentinel2"]).filterBounds(geom).filterDate("2017-03-28","2026-11-10")
        for season,a,b in [("dry",1,3),("post_monsoon",10,12),("all",1,12)]:
            coll=base.filter(ee.Filter.calendarRange(a,b,"month"))
            qa_features.append(ee.Feature(None,{"state":state,"season":season,"image_count":coll.size(),"mean_scene_cloud_pct":coll.aggregate_mean("CLOUDY_PIXEL_PERCENTAGE"),"metric_type":"scene_metadata_proxy","pixel_validity_status":"pending tiled SCL product"}))
        samples=feature_stack(cfg,geom).sample(region=geom,scale=5000,projection="EPSG:4326",geometries=False,tileScale=8,dropNulls=True)
        export=ee.batch.Export.table.toDrive(collection=samples,description=f"lostscape_features_{state.lower().replace(' ','_')}",folder="lostscape_south_private",fileNamePrefix=f"features_5km_{state.lower().replace(' ','_')}",fileFormat="CSV")
        export.start(); tasks.append({"kind":"features_5km","state":state,"task_id":export.id,"description":export.config.get("description")})
    qa=ee.batch.Export.table.toDrive(collection=ee.FeatureCollection(qa_features),description="lostscape_s2_scene_qa",folder="lostscape_south_private",fileNamePrefix="s2_scene_qa",fileFormat="CSV")
    qa.start(); tasks.append({"kind":"scene_qa","state":"all","task_id":qa.id,"description":qa.config.get("description")})
    return tasks


def main() -> None:
    cfg=yaml.safe_load((ROOT/"config.yaml").read_text()); ee.Initialize(project=cfg["gee"]["project"])
    records=submit(cfg); out=ROOT/"results/tasks"; out.mkdir(parents=True,exist_ok=True)
    stamp=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    (out/f"gee_tasks_{stamp}.json").write_text(json.dumps(records,indent=2))
    print(json.dumps(records,indent=2))


if __name__=="__main__": main()

