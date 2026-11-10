"""Model open-inventory documentation propensity and rank robust blind spots."""
from __future__ import annotations
from pathlib import Path
import hashlib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import average_precision_score,brier_score_loss,roc_auc_score
ROOT=Path(__file__).resolve().parents[2]; SEEDS=[11,29,47,71,101]
EXCLUDE={'latitude','longitude','label_positive','distance_to_known_megalith_km','block_x','block_y','spatial_block','system:index','.geo'}
def cid(lat:float,lon:float)->str: return hashlib.sha256(f'LostScape-v1:{int(np.floor(lat/.09))}:{int(np.floor(lon/.09))}'.encode()).hexdigest()[:12]
def main()->None:
 scores=pd.read_csv(ROOT/'results/tables/public_coarse_scores.csv'); grid=pd.read_csv(ROOT/'data/private/model_table.csv'); grid['cell_id_10km']=[cid(a,b) for a,b in zip(grid.latitude,grid.longitude)]; grid['state']=grid.feature_file.str.removeprefix('features_5km_').str.removesuffix('.csv').str.replace('_',' ').str.title()
 inv=pd.read_csv(ROOT/'data/private/master_inventory_precise.csv').dropna(subset=['lat','lon']); inv['cell_id_10km']=[cid(a,b) for a,b in zip(inv.lat,inv.lon)]
 effort=inv.groupby(['state','cell_id_10km']).agg(documented_sites=('source_id','nunique'),documented_sources=('source','nunique')).reset_index()
 numeric=[c for c in grid.select_dtypes(include=np.number) if c not in EXCLUDE]
 context=grid.groupby(['state','cell_id_10km'],as_index=False)[numeric].mean(); x=scores.merge(context,on=['state','cell_id_10km'],how='left').merge(effort,on=['state','cell_id_10km'],how='left').fillna({'documented_sites':0,'documented_sources':0}); x['documented']=(x.documented_sites>0).astype(int)
 feature_names=[c for c in numeric if c not in {'worldcover'}]; design=x[feature_names].copy(); design=pd.concat([design,pd.get_dummies(x.worldcover.round().astype('Int64'),prefix='landcover',dtype=float)],axis=1).replace([np.inf,-np.inf],np.nan).fillna(0)
 out_pred=np.zeros((len(SEEDS),len(x))); rows=[]
 for si,seed in enumerate(SEEDS):
  for held in sorted(x.state.unique()):
   tr=x.state.ne(held).to_numpy(); te=~tr; model=RandomForestClassifier(n_estimators=400,min_samples_leaf=10,class_weight='balanced_subsample',n_jobs=-1,random_state=seed).fit(design.loc[tr],x.loc[tr,'documented']); p=model.predict_proba(design.loc[te])[:,1]; out_pred[si,te]=p
   rows.append({'seed':seed,'held_out_state':held,'n_test':int(te.sum()),'documented_cells':int(x.loc[te,'documented'].sum()),'roc_auc':roc_auc_score(x.loc[te,'documented'],p),'pr_auc':average_precision_score(x.loc[te,'documented'],p),'brier':brier_score_loss(x.loc[te,'documented'],p)})
 x['documentation_propensity']=out_pred.mean(0); x['documentation_propensity_sd']=out_pred.std(0,ddof=1); x['probability_lower_90']=(x.probability-1.645*x.uncertainty).clip(0,1); x['blind_spot_score']=x.probability_lower_90*(1-x.documentation_propensity); x['definition']='lower-90% model score × (1 - out-of-state documentation propensity)'
 keep=['state','cell_id_10km','probability','probability_lower_90','uncertainty','documented_sites','documented_sources','documentation_propensity','documentation_propensity_sd','blind_spot_score','definition']
 candidates=x[x.documented_sites.eq(0)].sort_values(['state','blind_spot_score'],ascending=[True,False]).groupby('state').head(50); candidates[keep].to_csv(ROOT/'results/tables/survey_blind_spots.csv',index=False)
 pd.DataFrame(rows).to_csv(ROOT/'results/tables/survey_effort_model_cv.csv',index=False)
 stability=[]
 for state,g in x[x.documented_sites.eq(0)].groupby('state'):
  idx=g.index.to_numpy(); top_sets=[]
  for si in range(len(SEEDS)):
   score=g.probability_lower_90.to_numpy()*(1-out_pred[si,idx]); top_sets.append(set(g.iloc[np.argsort(-score)[:50]].cell_id_10km))
  jac=[len(top_sets[i]&top_sets[j])/len(top_sets[i]|top_sets[j]) for i in range(len(top_sets)) for j in range(i+1,len(top_sets))]
  stability.append({'state':state,'top_k':50,'mean_pairwise_jaccard':np.mean(jac),'min_pairwise_jaccard':np.min(jac)})
 pd.DataFrame(stability).to_csv(ROOT/'results/tables/survey_blind_spot_stability.csv',index=False)
 pd.DataFrame([{'limitation':'documentation propensity is not measured field-survey coverage','effect':'it models where open sources contain records, including digitization and institutional bias'},{'limitation':'roads and settlement distance are absent','effect':'accessibility correction is incomplete'},{'limitation':'candidate probability and effort model share environmental context','effect':'blind-spot score is a prioritization heuristic, not a causal estimate'}]).to_csv(ROOT/'results/tables/survey_blind_spot_limitations.csv',index=False)
 print({'cells':len(x),'documented_cells':int(x.documented.sum()),'candidate_cells':len(candidates)})
if __name__=='__main__': main()
