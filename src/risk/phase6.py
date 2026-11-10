"""Create site-protective coarse probability, uncertainty, risk and review products."""
from __future__ import annotations
from pathlib import Path
import hashlib
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from src.models.baselines import EXCLUDE

ROOT=Path(__file__).resolve().parents[2]; SEEDS=[11,29,47,71,101]
def cell_id(lat,lon):
    # 0.09 degrees is approximately 10 km north-south; IDs are irreversible hashes.
    a=int(np.floor(lat/.09)); b=int(np.floor(lon/.09))
    return hashlib.sha256(f'LostScape-v1:{a}:{b}'.encode()).hexdigest()[:12]
def main():
 (ROOT/'results/candidate_review').mkdir(parents=True,exist_ok=True); (ROOT/'results/maps').mkdir(parents=True,exist_ok=True)
 d=pd.read_csv(ROOT/'data/private/model_table.csv'); fs=[c for c in d.select_dtypes(include=np.number) if c not in EXCLUDE]
 pred=[]
 for seed in SEEDS:
  m=make_pipeline(SimpleImputer(),HistGradientBoostingClassifier(max_iter=150,l2_regularization=1,random_state=seed)).fit(d[fs],d.label_positive)
  pred.append(m.predict_proba(d[fs])[:,1])
 p=np.vstack(pred); d['probability']=p.mean(0); d['uncertainty']=p.std(0,ddof=1)
 d['crop_proxy']=d.worldcover.eq(40).astype(float); d['bare_proxy']=d.worldcover.eq(60).astype(float)
 d['threat_proxy']=np.clip(.6*d.built_probability+.3*d.crop_proxy+.1*d.bare_proxy,0,1)
 d['risk_score']=d.probability*d.threat_proxy
 d['state']=d.feature_file.str.removeprefix('features_5km_').str.removesuffix('.csv').str.replace('_',' ').str.title()
 d['cell_id_10km']=[cell_id(a,b) for a,b in zip(d.latitude,d.longitude)]
 agg=d.groupby(['state','cell_id_10km'],as_index=False).agg(probability=('probability','mean'),uncertainty=('uncertainty','mean'),threat_proxy=('threat_proxy','mean'),risk_score=('risk_score','mean'),known_positive_cells=('label_positive','sum'),cell_count=('label_positive','size'))
 out=ROOT/'results/tables'; out.mkdir(parents=True,exist_ok=True)
 agg.to_csv(out/'public_coarse_scores.csv',index=False)
 agg.sort_values(['state','risk_score'],ascending=[True,False]).groupby('state').head(50).to_csv(out/'top_risk_cells_per_state.csv',index=False)
 # Blinded review sheet: top-ranked candidates plus low-ranked controls; no precise coordinates.
 rng=np.random.default_rng(20261110); top=agg[agg.known_positive_cells.eq(0)].sort_values('probability',ascending=False).head(80).sample(40,random_state=20261110)
 low=agg[agg.known_positive_cells.eq(0)].sort_values('probability').head(400).sample(20,random_state=20261110)
 review=pd.concat([top.assign(hidden_stratum='top'),low.assign(hidden_stratum='control')]).sample(frac=1,random_state=20261110).reset_index(drop=True)
 review['review_id']=[f'LSR-{i:03d}' for i in range(1,len(review)+1)]
 review[['review_id','state','cell_id_10km']].assign(reviewer='',rating='',notes='').to_csv(ROOT/'results/candidate_review/review_sheet.csv',index=False)
 review[['review_id','hidden_stratum','probability','uncertainty']].to_csv(ROOT/'data/private/review_key_private.csv',index=False)
 # Heuristic failure audit; these are diagnostic categories, not visually verified causes.
 high=d.sort_values('probability',ascending=False).head(max(100,int(.01*len(d))))
 pd.DataFrame([{'diagnostic':'high-score cells with built_probability > 0.25','count':int((high.built_probability>.25).sum())},{'diagnostic':'high-score cropland cells','count':int(high.worldcover.eq(40).sum())},{'diagnostic':'known-positive cells below median score','count':int(((d.label_positive.eq(1))&(d.probability<d.probability.median())).sum())}]).to_csv(out/'failure_diagnostics.csv',index=False)
 # Generalized maps use 10-km cell aggregates only.
 coords=d.groupby(['state','cell_id_10km'],as_index=False).agg(latitude=('latitude','mean'),longitude=('longitude','mean'))
 mp=agg.merge(coords,on=['state','cell_id_10km']); borders=gpd.read_file(ROOT/'data/raw/boundaries_ind_adm1.geojson')
 for col,name in [('probability','probability_map'),('uncertainty','uncertainty_map'),('risk_score','risk_priority_map')]:
  fig,ax=plt.subplots(figsize=(7,8)); borders[borders.shapeName.isin(['Karnataka','Andhra Pradesh','Tamil Nadu','Kerala'])].boundary.plot(ax=ax,color='0.4',linewidth=.6)
  sc=ax.scatter(mp.longitude,mp.latitude,c=mp[col],s=5,cmap='viridis'); fig.colorbar(sc,ax=ax,label=col.replace('_',' ')); ax.set_axis_off(); fig.tight_layout(); fig.savefig(ROOT/f'results/maps/{name}.png',dpi=300); fig.savefig(ROOT/f'results/maps/{name}.pdf'); plt.close(fig)
if __name__=='__main__': main()
