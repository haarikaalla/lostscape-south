"""Retrospective pseudo-discovery tests on wholly withheld known-site clusters."""
from __future__ import annotations
from pathlib import Path
import hashlib
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.neighbors import BallTree
from sklearn.pipeline import make_pipeline
from scipy.stats import wilcoxon
from src.eval.metrics import ranking_metrics
from src.models.baselines import EXCLUDE
ROOT=Path(__file__).resolve().parents[2]; R=6371.0088; SEEDS=[11,29,47,71,101]

def radial(lat,lon,a,b): return np.hypot((lat-a)*111.32,(lon-b)*111.32*np.cos(np.radians((lat+a)/2)))

def main()->None:
 d=pd.read_csv(ROOT/'data/private/model_table.csv'); sites=pd.read_csv(ROOT/'data/private/master_inventory_precise.csv').dropna(subset=['lat','lon']).copy(); fs=[c for c in d.select_dtypes(include=np.number) if c not in EXCLUDE]
 alltree=BallTree(np.radians(sites[['lat','lon']]),metric='haversine'); near,_=alltree.query(np.radians(d[['latitude','longitude']]),k=1); d['broad_label']=(near[:,0]*R<=3.6).astype(int)
 chosen=[]
 for state,g in sites.groupby('state'):
  labels=DBSCAN(eps=10/R,min_samples=3,metric='haversine').fit_predict(np.radians(g[['lat','lon']])); g=g.assign(cluster=labels)
  eligible=g[g.cluster.ge(0)].groupby('cluster').agg(site_records=('source_id','nunique'),class_count=('class','nunique'),lat=('lat','mean'),lon=('lon','mean')).reset_index(); eligible=eligible[(eligible.site_records>=4)&(eligible.class_count>=2)].sort_values(['site_records','class_count'],ascending=False).head(3)
  for r in eligible.itertuples():
   members=g[g.cluster.eq(r.cluster)]; key=hashlib.sha256((state+':'+'|'.join(sorted(members.source_id.astype(str)))).encode()).hexdigest()[:12]; chosen.append((state,int(r.cluster),key,members,float(r.lat),float(r.lon),int(r.site_records),int(r.class_count)))
 rows=[]; rng=np.random.default_rng(20261110)
 for state,cluster,key,members,clat,clon,n_sites,n_classes in chosen:
  rd=radial(d.latitude.to_numpy(),d.longitude.to_numpy(),clat,clon); train=rd>75; test=rd<=30
  target_tree=BallTree(np.radians(members[['lat','lon']]),metric='haversine'); td,_=target_tree.query(np.radians(d.loc[test,['latitude','longitude']]),k=1); y=(td[:,0]*R<=3.6).astype(int)
  if y.sum()==0: continue
  for seed in SEEDS:
   m=make_pipeline(SimpleImputer(),HistGradientBoostingClassifier(max_iter=150,l2_regularization=1,random_state=seed)).fit(d.loc[train,fs],d.loc[train,'broad_label']); p=m.predict_proba(d.loc[test,fs])[:,1]
   ranks=np.argsort(np.argsort(-p))[y==1]+1; rows.append({'state':state,'cluster_id':key,'method':'full_hgb','seed':seed,'source_records':n_sites,'class_count':n_classes,'train_buffer_km':75,'test_radius_km':30,'test_cells':len(y),'target_cells':int(y.sum()),'median_target_rank':float(np.median(ranks)),'median_target_percentile':float(1-np.median(ranks)/len(y)),**ranking_metrics(y,p)})
  remaining=sites[radial(sites.lat.to_numpy(),sites.lon.to_numpy(),clat,clon)>75]; tree=BallTree(np.radians(remaining[['lat','lon']]),metric='haversine'); dd,_=tree.query(np.radians(d.loc[test,['latitude','longitude']]),k=1); p=-dd[:,0]; ranks=np.argsort(np.argsort(-p))[y==1]+1; rows.append({'state':state,'cluster_id':key,'method':'distance_to_remaining_known','seed':-1,'source_records':n_sites,'class_count':n_classes,'train_buffer_km':75,'test_radius_km':30,'test_cells':len(y),'target_cells':int(y.sum()),'median_target_rank':float(np.median(ranks)),'median_target_percentile':float(1-np.median(ranks)/len(y)),**ranking_metrics(y,p)})
  for seed in range(100):
   p=rng.random(len(y)); ranks=np.argsort(np.argsort(-p))[y==1]+1; rows.append({'state':state,'cluster_id':key,'method':'random','seed':seed,'source_records':n_sites,'class_count':n_classes,'train_buffer_km':75,'test_radius_km':30,'test_cells':len(y),'target_cells':int(y.sum()),'median_target_rank':float(np.median(ranks)),'median_target_percentile':float(1-np.median(ranks)/len(y)),**ranking_metrics(y,p)})
 result=pd.DataFrame(rows); out=ROOT/'results/tables'; result.to_csv(out/'pseudo_discovery_cluster_tests.csv',index=False)
 summary=result.groupby(['state','method']).agg(clusters=('cluster_id','nunique'),runs=('seed','size'),pr_auc=('pr_auc','mean'),recall_top_1pct=('recall_top_1pct','mean'),recall_top_5pct=('recall_top_5pct','mean'),recall_top_10pct=('recall_top_10pct','mean'),median_target_percentile=('median_target_percentile','median')).reset_index(); summary.to_csv(out/'pseudo_discovery_summary.csv',index=False)
 cluster=result.groupby(['cluster_id','method']).agg(pr_auc=('pr_auc','mean'),recall_top_10pct=('recall_top_10pct','mean')).reset_index(); full=cluster[cluster.method.eq('full_hgb')].set_index('cluster_id'); random=cluster[cluster.method.eq('random')].set_index('cluster_id'); sig=[]
 for metric in ['pr_auc','recall_top_10pct']:
  a=full.loc[random.index,metric].to_numpy(); b=random[metric].to_numpy(); stat,p=wilcoxon(a,b,alternative='greater'); sig.append({'comparison':f'full_hgb > random cluster mean: {metric}','clusters':len(a),'mean_full':a.mean(),'mean_random':b.mean(),'mean_difference':(a-b).mean(),'wilcoxon_statistic':stat,'one_sided_p':p})
 pd.DataFrame(sig).to_csv(out/'pseudo_discovery_significance.csv',index=False)
 pd.DataFrame([{'interpretation':'retrospective pseudo-discovery only','supported':True,'detail':'whole known clusters were excluded with a 75-km buffer before ranking a 30-km test area'},{'interpretation':'prospective archaeological discovery','supported':False,'detail':'no candidate has independent expert or field verification'},{'interpretation':'lost city or empire','supported':False,'detail':'cluster recovery cannot establish identity, chronology, urban scale or political affiliation'},{'interpretation':'small or isolated site generalization','supported':False,'detail':'stress test preselects up to three dense multi-class clusters per state'}]).to_csv(out/'pseudo_discovery_scope.csv',index=False)
 print({'clusters':result.cluster_id.nunique(),'states':result.state.nunique(),'full_runs':int(result.method.eq('full_hgb').sum())})
if __name__=='__main__': main()
