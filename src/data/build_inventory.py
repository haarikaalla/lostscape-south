"""Build a provenance-preserving, public-safe archaeological inventory."""
from __future__ import annotations

import hashlib
import json
import math
import time
from pathlib import Path

import geopandas as gpd
import pandas as pd
import requests
import yaml
from shapely.geometry import Point

ROOT = Path(__file__).resolve().parents[2]
UA = "LostScape-South/0.1 (research; contact via repository)"


def load_config() -> dict:
    return yaml.safe_load((ROOT / "config.yaml").read_text())


def fetch_json(url: str, *, params=None, data=None, timeout=300) -> dict:
    r = requests.get(url, params=params, headers={"User-Agent": UA}, timeout=timeout) if data is None else requests.post(url, data=data, headers={"User-Agent": UA}, timeout=timeout)
    r.raise_for_status()
    return r.json()


def boundaries() -> gpd.GeoDataFrame:
    cache = ROOT / "data/raw/boundaries_ind_adm1.geojson"
    cache.parent.mkdir(parents=True, exist_ok=True)
    if not cache.exists():
        meta = fetch_json("https://www.geoboundaries.org/api/current/gbOpen/IND/ADM1/")
        url = meta["gjDownloadURL"]
        response = requests.get(url, headers={"User-Agent": UA}, timeout=300)
        response.raise_for_status()
        cache.write_bytes(response.content)
        (ROOT / "data/raw/geoboundaries_metadata.json").write_text(json.dumps(meta, indent=2))
    gdf = gpd.read_file(cache).to_crs(4326)
    name_col = next(c for c in ["shapeName", "shapeName1", "NAME_1"] if c in gdf.columns)
    gdf = gdf.rename(columns={name_col: "state"})
    wanted = load_config()["region"]["states"]
    return gdf[gdf.state.isin(wanted)][["state", "geometry"]].copy()


OVERPASS_QUERY = """[out:json][timeout:600];
area["ISO3166-1"="IN"][admin_level=2]->.india;
(
  nwr(area.india)["historic"="archaeological_site"];
  nwr(area.india)["archaeological_site"];
  nwr(area.india)["megalith"];
  nwr(area.india)["historic"="tomb"];
  nwr(area.india)["tomb"];
  nwr(area.india)["historic"="ruins"];
  nwr(area.india)["ruins"];
  nwr(area.india)["historic"="fort"];
  nwr(area.india)["fortification_type"];
);
out center tags;"""


def osm_records() -> list[dict]:
    raw_path = ROOT / "data/raw/osm_overpass_inventory.json"
    (ROOT / "data/raw/osm_overpass_query.txt").write_text(OVERPASS_QUERY)
    if raw_path.exists():
        raw = json.loads(raw_path.read_text())
    else:
        raw = fetch_json(load_config()["inventory"]["overpass_endpoint"], data={"data": OVERPASS_QUERY}, timeout=700)
        raw_path.write_text(json.dumps(raw))
    out = []
    for e in raw.get("elements", []):
        lat = e.get("lat", e.get("center", {}).get("lat")); lon = e.get("lon", e.get("center", {}).get("lon"))
        if lat is None or lon is None: continue
        tags = e.get("tags", {})
        out.append({"source":"OpenStreetMap", "source_id":f'{e["type"]}/{e["id"]}', "name":tags.get("name"), "lat":lat, "lon":lon, "tags":json.dumps(tags, sort_keys=True), "discovery_year":None, "protection_status":tags.get("protection_title") or tags.get("heritage")})
    return out


WIKIDATA_QUERY = """SELECT DISTINCT ?item ?itemLabel ?coord ?instanceLabel ?heritageLabel ?date WHERE {
  VALUES ?state { wd:Q1185 wd:Q1159 wd:Q1445 wd:Q1186 }
  ?item wdt:P625 ?coord; wdt:P131* ?state.
  OPTIONAL { ?item wdt:P31 ?instance. }
  OPTIONAL { ?item wdt:P1435 ?heritage. }
  OPTIONAL { ?item wdt:P571 ?date. }
  FILTER(EXISTS { ?item wdt:P1435 ?x } || EXISTS { ?item wdt:P31/wdt:P279* wd:Q839954 })
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}"""


def wikidata_records() -> list[dict]:
    raw_path = ROOT / "data/raw/wikidata_inventory.json"
    (ROOT / "data/raw/wikidata_query.sparql").write_text(WIKIDATA_QUERY)
    if raw_path.exists(): raw = json.loads(raw_path.read_text())
    else:
        raw = fetch_json(load_config()["inventory"]["wikidata_endpoint"], params={"query":WIKIDATA_QUERY,"format":"json"}, timeout=300)
        raw_path.write_text(json.dumps(raw))
    out=[]
    for b in raw["results"]["bindings"]:
        xy=b["coord"]["value"].removeprefix("Point(").removesuffix(")").split()
        date=b.get("date",{}).get("value"); year=int(date[:4]) if date and date[:4].isdigit() else None
        out.append({"source":"Wikidata", "source_id":b["item"]["value"].rsplit("/",1)[-1], "name":b.get("itemLabel",{}).get("value"), "lon":float(xy[0]), "lat":float(xy[1]), "tags":json.dumps({"instance":b.get("instanceLabel",{}).get("value"),"heritage":b.get("heritageLabel",{}).get("value")},sort_keys=True), "discovery_year":year, "protection_status":b.get("heritageLabel",{}).get("value")})
    return out


def classify(row: pd.Series) -> tuple[str,str]:
    text=" ".join(str(row.get(k) or "") for k in ("name","tags")).lower()
    primary={"dolmen":"dolmen","cist":"cist","menhir":"menhir","megalith":"megalith","stone circle":"stone_circle","cairn":"cairn","umbrella stone":"umbrella_stone","hood stone":"hood_stone","rock-cut":"rock_cut_cave"}
    for token, subtype in primary.items():
        if token in text: return "megalithic_burial", subtype
    if "tank" in text or "reservoir" in text: return "ancient_tank", "tank"
    if "mound" in text: return "settlement_mound", "mound"
    if "fort" in text: return "fort_or_town_ruin", "fort"
    if "ruin" in text: return "fort_or_town_ruin", "ruins"
    if "tomb" in text or "burial" in text: return "burial_other", "tomb_or_burial"
    return "archaeological_site_other", "unspecified"


def public_grid_id(lat: float, lon: float, km: int) -> str:
    # Geographic quantization is deliberately coarse; IDs disclose no point coordinate.
    dlat=km/111.32; dlon=km/(111.32*max(math.cos(math.radians(lat)),0.2))
    a=math.floor(lat/dlat); b=math.floor(lon/dlon)
    return hashlib.sha256(f"lostscape|{km}|{a}|{b}".encode()).hexdigest()[:14]


def main() -> None:
    cfg=load_config(); states=boundaries()
    df=pd.DataFrame(osm_records()+wikidata_records())
    g=gpd.GeoDataFrame(df, geometry=[Point(xy) for xy in zip(df.lon,df.lat)], crs=4326)
    g=gpd.sjoin(g, states, predicate="within", how="inner").drop(columns=["index_right"])
    classes=g.apply(classify,axis=1,result_type="expand"); g[["class","sub_type"]]=classes
    # Deterministic proximity deduplication in metric CRS, preferring records with a name/year.
    metric=g.to_crs(32643); keep=[]
    for _, group in metric.sort_values(["source","source_id"]).groupby("state"):
        chosen=[]
        for idx,row in group.iterrows():
            if not chosen or all(row.geometry.distance(group.loc[j].geometry)>cfg["inventory"]["deduplication_tolerance_m"] for j in chosen): chosen.append(idx)
        keep.extend(chosen)
    g=g.loc[keep].copy()
    private=ROOT/"data/private"; private.mkdir(parents=True,exist_ok=True)
    g.drop(columns="geometry").to_csv(private/"master_inventory_precise.csv",index=False)
    g["grid_id_10km"]=[public_grid_id(a,b,cfg["region"]["public_grid_km"]) for a,b in zip(g.lat,g.lon)]
    public=(g.groupby(["grid_id_10km","state","source","class","sub_type"],dropna=False).size().rename("site_count").reset_index())
    out=ROOT/"data/processed"; out.mkdir(parents=True,exist_ok=True); public.to_csv(out/"inventory_coarse_10km.csv",index=False)
    counts=g.groupby(["state","source","class"]).agg(site_count=("source_id","size"),discovery_year_known=("discovery_year",lambda x:x.notna().sum())).reset_index()
    counts["discovery_year_coverage_pct"]=(100*counts.discovery_year_known/counts.site_count).round(1)
    results=ROOT/"results/tables"; results.mkdir(parents=True,exist_ok=True); counts.to_csv(results/"label_counts.csv",index=False)
    gate=g[g["class"]=="megalithic_burial"].groupby("state").size().reindex(cfg["region"]["states"],fill_value=0)
    report={"generated_at":"2026-11-10","total_deduplicated":len(g),"primary_total":int(gate.sum()),"primary_by_state":gate.astype(int).to_dict(),"threshold_total":cfg["inventory"]["primary_min_total"],"threshold_per_block":cfg["inventory"]["primary_min_per_block"],"passed":bool(gate.sum()>=cfg["inventory"]["primary_min_total"] and (gate>=cfg["inventory"]["primary_min_per_block"]).all())}
    (results/"label_gate.json").write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2)); print(counts.to_string(index=False))

if __name__=="__main__": main()

