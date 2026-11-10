"""Phase-5 experiments supported by the coarse private feature table."""
from __future__ import annotations
from pathlib import Path
import json
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from src.eval.metrics import ranking_metrics
from src.models.baselines import EXCLUDE

ROOT=Path(__file__).resolve().parents[2]; SEEDS=[11,29,47,71,101]

def hgb(seed:int): return make_pipeline(SimpleImputer(),HistGradientBoostingClassifier(max_iter=150,l2_regularization=1,random_state=seed))

def main():
 d=pd.read_csv(ROOT/'data/private/model_table.csv'); nums=[c for c in d.select_dtypes(include=np.number) if c not in EXCLUDE]
 groups={
  'all':nums,
  'remove_crop_mark':[c for c in nums if not any(x in c for x in ('ndvi','ndwi','evi'))],
  'remove_sar':[c for c in nums if not c.startswith(('vv_','vh_'))],
  'remove_terrain':[c for c in nums if c not in ('elevation_m','slope','aspect')],
  'remove_time_variability':[c for c in nums if not c.endswith(('_sd','valid_n'))],
  'remove_landcover':[c for c in nums if c!='worldcover'],
 }
 abl=[]
 for seed in SEEDS:
  for held in sorted(d.feature_file.unique()):
   tr=d.feature_file.ne(held); te=~tr
   for name,fs in groups.items():
    m=hgb(seed).fit(d.loc[tr,fs],d.loc[tr,'label_positive']); p=m.predict_proba(d.loc[te,fs])[:,1]
    abl.append({'seed':seed,'held_out':held,'ablation':name,'n_features':len(fs),**ranking_metrics(d.loc[te,'label_positive'].to_numpy(),p)})
 pd.DataFrame(abl).to_csv(ROOT/'results/tables/ablations.csv',index=False)

 # Feature variograms from deterministic within-state pairs; range is first bin reaching 95% of sampled sill.
 rng=np.random.default_rng(20261110); vg=[]; ranges=[]; bins=np.arange(0,325,25)
 for feature in ['elevation_m','dry_ndvi_med','built_probability','rain_daily_mean_mm']:
  allsemi=[]
  for state,g in d.groupby('feature_file'):
   n=min(1200,len(g)); s=g.sample(n,random_state=20261110); a=rng.integers(0,n,12000); b=rng.integers(0,n,12000)
   lat=s.latitude.to_numpy(); lon=s.longitude.to_numpy(); x=s[feature].to_numpy()
   dy=(lat[a]-lat[b])*111.32; dx=(lon[a]-lon[b])*111.32*np.cos(np.radians((lat[a]+lat[b])/2)); dist=np.hypot(dx,dy); semi=.5*(x[a]-x[b])**2
   for lo,hi in zip(bins[:-1],bins[1:]):
    z=(dist>=lo)&(dist<hi)
    if z.any(): vg.append({'feature':feature,'state_file':state,'distance_mid_km':(lo+hi)/2,'semivariance':float(semi[z].mean()),'pairs':int(z.sum())})
   allsemi.extend(semi[dist<300].tolist())
  q=pd.DataFrame([r for r in vg if r['feature']==feature]).groupby('distance_mid_km').semivariance.mean(); sill=np.mean(allsemi)
  reached=q[q>=.95*sill]; ranges.append({'feature':feature,'sampled_sill':sill,'range_km':float(reached.index.min()) if len(reached) else 300.0,'method':'sampled empirical variogram; 95% sill'})
 pd.DataFrame(vg).to_csv(ROOT/'results/tables/feature_variograms.csv',index=False); pd.DataFrame(ranges).to_csv(ROOT/'results/tables/autocorrelation_ranges.csv',index=False)

 # Leave-one-land-cover-out on classes with at least five observed positives.
 lc=[]
 for cover,g in d.groupby('worldcover'):
  if g.label_positive.sum()<5: continue
  tr=d.worldcover.ne(cover); te=~tr
  for seed in SEEDS:
   m=hgb(seed).fit(d.loc[tr,nums],d.loc[tr,'label_positive']); p=m.predict_proba(d.loc[te,nums])[:,1]
   lc.append({'seed':seed,'held_out_worldcover':int(cover),'test_n':int(te.sum()),'test_positives':int(d.loc[te,'label_positive'].sum()),**ranking_metrics(d.loc[te,'label_positive'].to_numpy(),p)})
 pd.DataFrame(lc).to_csv(ROOT/'results/tables/landcover_transfer.csv',index=False)

 # Availability records: no megalithic discovery dates and no licensed lithology layer ingested yet.
 pd.DataFrame([{'module':'temporal_holdout','status':'not_estimable','available_primary_dates':0,'required_action':'obtain documented discovery/publication dates from approved open sources'}, {'module':'geology_transfer','status':'not_run','available_geology_feature':False,'required_action':'ingest and license-check an open lithology layer'}]).to_csv(ROOT/'results/tables/unavailable_experiments.csv',index=False)
 print(json.dumps({'ablation_runs':len(abl),'landcover_runs':len(lc),'ranges':ranges},indent=2))
if __name__=='__main__': main()
