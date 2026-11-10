"""Spatially withheld tests for verified settlement-mound records where available."""
from pathlib import Path
import numpy as np,pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.neighbors import BallTree
from sklearn.pipeline import make_pipeline
from src.eval.metrics import ranking_metrics
from src.models.baselines import EXCLUDE
ROOT=Path(__file__).resolve().parents[2]; R=6371.0088
TARGETS={'Andhra Pradesh':"Mound known as 'bodipati dibba'",'Karnataka':'Fortified Mound near Sannathi?','Tamil Nadu':'Mandapakkadu (Structure with mound)'}
def dist(lat,lon,a,b): return np.hypot((lat-a)*111.32,(lon-b)*111.32*np.cos(np.radians((lat+a)/2)))
def main():
 d=pd.read_csv(ROOT/'data/private/model_table.csv'); sites=pd.read_csv(ROOT/'data/private/master_inventory_precise.csv').dropna(subset=['lat','lon']); fs=[c for c in d.select_dtypes(include=np.number) if c not in EXCLUDE]
 alltree=BallTree(np.radians(sites[['lat','lon']]),metric='haversine'); dd,_=alltree.query(np.radians(d[['latitude','longitude']]),k=1); d['broad_label']=(dd[:,0]*R<=3.6).astype(int)
 rows=[]; rng=np.random.default_rng(20261110)
 for state,name in TARGETS.items():
  q=sites[(sites.state.eq(state))&(sites.name.eq(name))].iloc[0]; radial=dist(d.latitude.to_numpy(),d.longitude.to_numpy(),q.lat,q.lon); train=radial>75; test=radial<=40; target=np.argmin(radial[test]); yt=d.loc[test,'broad_label'].to_numpy(); xt=d.loc[test,fs]
  for seed in [11,29,47,71,101]:
   m=make_pipeline(SimpleImputer(),HistGradientBoostingClassifier(max_iter=150,l2_regularization=1,random_state=seed)).fit(d.loc[train,fs],d.loc[train,'broad_label']); p=m.predict_proba(xt)[:,1]; rank=int(np.argsort(np.argsort(-p))[target]+1)
   rows.append({'state':state,'site_name':name,'method':'full_hgb','seed':seed,'test_n':len(yt),'test_known_cells':int(yt.sum()),'target_cell_rank':rank,'target_cell_percentile':1-rank/len(yt),**ranking_metrics(yt,p)})
  outside=sites[dist(sites.lat.to_numpy(),sites.lon.to_numpy(),q.lat,q.lon)>75]; tree=BallTree(np.radians(outside[['lat','lon']]),metric='haversine'); near,_=tree.query(np.radians(d.loc[test,['latitude','longitude']]),k=1); score=-near[:,0]
  rank=int(np.argsort(np.argsort(-score))[target]+1); rows.append({'state':state,'site_name':name,'method':'distance_to_known_site','seed':-1,'test_n':len(yt),'test_known_cells':int(yt.sum()),'target_cell_rank':rank,'target_cell_percentile':1-rank/len(yt),**ranking_metrics(yt,score)})
  for i in range(100):
   p=rng.random(len(yt)); rank=int(np.argsort(np.argsort(-p))[target]+1); rows.append({'state':state,'site_name':name,'method':'random','seed':i,'test_n':len(yt),'test_known_cells':int(yt.sum()),'target_cell_rank':rank,'target_cell_percentile':1-rank/len(yt),**ranking_metrics(yt,p)})
 pd.DataFrame(rows).to_csv(ROOT/'results/tables/lost_settlement_holdouts.csv',index=False)
 pd.DataFrame([{'state':'Kerala','status':'insufficient data','reason':'verified inventory contains no settlement_mound record'},{'baseline':'distance_to_river_only','status':'not run','reason':'river-distance feature not yet ingested'}]).to_csv(ROOT/'results/tables/lost_settlement_holdout_limitations.csv',index=False)
if __name__=='__main__': main()
