"""Rank generalized high-score cells with low open-inventory documentation density."""
from pathlib import Path
import hashlib,numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[2]
def cid(lat,lon): return hashlib.sha256(f'LostScape-v1:{int(np.floor(lat/.09))}:{int(np.floor(lon/.09))}'.encode()).hexdigest()[:12]
def main():
 s=pd.read_csv(ROOT/'results/tables/public_coarse_scores.csv'); inv=pd.read_csv(ROOT/'data/private/master_inventory_precise.csv').dropna(subset=['lat','lon']); inv['cell_id_10km']=[cid(a,b) for a,b in zip(inv.lat,inv.lon)]
 effort=inv.groupby(['state','cell_id_10km']).agg(documented_sites=('source_id','nunique'),documented_sources=('source','nunique')).reset_index()
 x=s.merge(effort,on=['state','cell_id_10km'],how='left').fillna({'documented_sites':0,'documented_sources':0}); x['documentation_density_proxy']=x.documented_sites; x['blind_spot_score']=x.probability/(1+x.documentation_density_proxy); x['definition']='high model score / (1 + open-inventory records in generalized cell)'
 x.sort_values(['state','blind_spot_score'],ascending=[True,False]).groupby('state').head(50).to_csv(ROOT/'results/tables/survey_blind_spots.csv',index=False)
 pd.DataFrame([{'limitation':'documentation density is not measured survey effort','effect':'cells may have been surveyed but not digitized in the three inventory sources'},{'limitation':'accessibility and road-distance effort model unavailable','effect':'ranking is a documentation blind-spot proxy, not a causal survey-bias correction'}]).to_csv(ROOT/'results/tables/survey_blind_spot_limitations.csv',index=False)
if __name__=='__main__': main()
