"""Withheld Vijayanagara/Hampi coarse validation using the broader inventory target."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.neighbors import BallTree
from sklearn.pipeline import make_pipeline
from src.eval.metrics import ranking_metrics
from src.models.baselines import EXCLUDE
ROOT=Path(__file__).resolve().parents[2]
HAMPI=np.array([15.335,76.460]); R=6371.0088
def km(lat,lon):
 y=(lat-HAMPI[0])*111.32; x=(lon-HAMPI[1])*111.32*np.cos(np.radians((lat+HAMPI[0])/2)); return np.hypot(x,y)
def main():
 d=pd.read_csv(ROOT/'data/private/model_table.csv'); sites=pd.read_csv(ROOT/'data/private/master_inventory_precise.csv').dropna(subset=['lat','lon'])
 tree=BallTree(np.radians(sites[['lat','lon']]),metric='haversine'); dist,_=tree.query(np.radians(d[['latitude','longitude']]),k=1)
 d['broad_label']=(dist[:,0]*R<=3.6).astype(int); d['hampi_distance_km']=km(d.latitude.to_numpy(),d.longitude.to_numpy())
 train=d.hampi_distance_km.gt(75); test=d.hampi_distance_km.le(40)
 fs=[c for c in d.select_dtypes(include=np.number) if c not in EXCLUDE|{'broad_label','hampi_distance_km'}]
 rows=[]; ps=[]
 for seed in [11,29,47,71,101]:
  m=make_pipeline(SimpleImputer(),HistGradientBoostingClassifier(max_iter=150,l2_regularization=1,random_state=seed)).fit(d.loc[train,fs],d.loc[train,'broad_label'])
  p=m.predict_proba(d.loc[test,fs])[:,1]; ps.append(p); rows.append({'seed':seed,'train_n':int(train.sum()),'test_n':int(test.sum()),'test_known_cells':int(d.loc[test,'broad_label'].sum()),**ranking_metrics(d.loc[test,'broad_label'].to_numpy(),p)})
 out=ROOT/'results/tables'; pd.DataFrame(rows).to_csv(out/'hampi_withheld_case.csv',index=False)
 z=d.loc[test,['latitude','longitude','broad_label']].copy(); z['probability']=np.mean(ps,axis=0); z['uncertainty']=np.std(ps,axis=0,ddof=1); z.to_csv(ROOT/'data/private/hampi_predictions_private.csv',index=False)
if __name__=='__main__': main()
