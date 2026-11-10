"""Render a public-safe density map; no point locations are plotted."""
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]


def main() -> None:
    sites=pd.read_csv(ROOT/"data/private/master_inventory_precise.csv")
    # Aggregate to ~10 km cells before drawing. Exact points never enter the figure.
    sites["cell_lon"]=(sites.lon/0.1).round()*0.1
    sites["cell_lat"]=(sites.lat/0.1).round()*0.1
    density=sites.groupby(["cell_lon","cell_lat"]).size().rename("count").reset_index()
    states=gpd.read_file(ROOT/"data/raw/boundaries_ind_adm1.geojson")
    keep=states.shapeName.str.normalize("NFKD").str.encode("ascii",errors="ignore").str.decode("ascii").isin(["Karnataka","Andhra Pradesh","Tamil Nadu","Kerala"])
    states=states[keep]
    fig,ax=plt.subplots(figsize=(8,10),layout="constrained")
    states.plot(ax=ax,color="#f4efe6",edgecolor="#3f4a4d",linewidth=.8)
    sc=ax.scatter(density.cell_lon,density.cell_lat,c=density["count"],s=20+12*density["count"].clip(upper=20),cmap="magma_r",alpha=.82,marker="s",linewidth=0)
    cb=fig.colorbar(sc,ax=ax,shrink=.65); cb.set_label("Documented sites per generalized ~10 km cell")
    ax.set(title="LostScape-South master inventory coverage",xlabel="Longitude (generalized)",ylabel="Latitude (generalized)")
    ax.text(.01,.01,"Sources: OpenStreetMap and Wikidata; accessed 2026-11-10.\nCells show aggregated documentation density, not survey-complete absence.",transform=ax.transAxes,fontsize=8,va="bottom")
    out=ROOT/"results/figures"; out.mkdir(parents=True,exist_ok=True)
    fig.savefig(out/"inventory_coverage_coarse.png",dpi=300)
    fig.savefig(out/"inventory_coverage_coarse.pdf")


if __name__=="__main__": main()
