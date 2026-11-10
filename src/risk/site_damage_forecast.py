"""Backtest and forecast construction-pressure trends; never labels them site damage."""
from pathlib import Path
import hashlib
import numpy as np,pandas as pd
from scipy.stats import linregress,spearmanr,t
ROOT=Path(__file__).resolve().parents[2]
def cid(lat,lon): return hashlib.sha256(f'LostScape-v1:{int(np.floor(lat/.09))}:{int(np.floor(lon/.09))}'.encode()).hexdigest()[:12]
def ci_boot(a,fn,seed=20261110):
 rng=np.random.default_rng(seed); vals=[]; n=len(a)
 for _ in range(1000): vals.append(fn(a.iloc[rng.integers(0,n,n)]))
 return np.quantile(vals,[.025,.975])
def main():
 p=ROOT/'data/private/site_damage_history_2016_2025.csv'; d=pd.read_csv(p); wide=d.pivot(index=['site_key','state'],columns='year',values='built_probability').dropna().reset_index(); rows=[]
 for _,r in wide.iterrows():
  vals=np.array([r[y] for y in range(2016,2026)],float)
  early=linregress(np.arange(2016,2021),vals[:5]); full=linregress(np.arange(2016,2026),vals); crit=t.ppf(.975,8)
  rows.append({'site_key':r.site_key,'state':r.state,'built_2025':vals[-1],'predicted_change_2020_2025':early.slope*5,'observed_change_2020_2025':vals[-1]-vals[4],'slope_per_year':full.slope,'slope_ci95_low':full.slope-crit*full.stderr,'slope_ci95_high':full.slope+crit*full.stderr,'forecast_built_2030':np.clip(vals[-1]+5*full.slope,0,1),'forecast_built_2035':np.clip(vals[-1]+10*full.slope,0,1),'projected_increase_5yr':5*full.slope})
 z=pd.DataFrame(rows); inv=pd.read_csv(ROOT/'data/private/master_inventory_precise.csv').dropna(subset=['lat','lon']); inv['site_key']=[hashlib.sha256(f'{a}:{b}'.encode()).hexdigest()[:16] for a,b in zip(inv.source,inv.source_id)]; inv['cell_id_10km']=[cid(a,b) for a,b in zip(inv.lat,inv.lon)]; z=z.merge(inv[['site_key','cell_id_10km']],on='site_key',how='left')
 metrics=[]
 for state,g in list(z.groupby('state'))+[('All states',z)]:
  rho=spearmanr(g.predicted_change_2020_2025,g.observed_change_2020_2025).statistic; mae=np.mean(abs(g.predicted_change_2020_2025-g.observed_change_2020_2025)); lo,hi=ci_boot(g,lambda q:np.mean(abs(q.predicted_change_2020_2025-q.observed_change_2020_2025)))
  metrics.append({'state':state,'sites':len(g),'spearman_rank_correlation':rho,'mae':mae,'mae_ci95_low':lo,'mae_ci95_high':hi,'backtest_train_years':'2016-2020','backtest_target':'2020-2025 built-probability change'})
 out=ROOT/'results/tables'; pd.DataFrame(metrics).to_csv(out/'site_damage_forecast_backtest.csv',index=False)
 cell=z.groupby(['state','cell_id_10km'],as_index=False).agg(site_count=('site_key','nunique'),built_2025=('built_2025','mean'),forecast_built_2030=('forecast_built_2030','mean'),forecast_built_2035=('forecast_built_2035','mean'),projected_increase_5yr=('projected_increase_5yr','mean'),slope_ci95_low=('slope_ci95_low','mean'),slope_ci95_high=('slope_ci95_high','mean'))
 cell['forecast_pressure_score']=cell.forecast_built_2030.clip(0,1); cell.sort_values(['state','forecast_pressure_score'],ascending=[True,False]).groupby('state').head(50).to_csv(out/'site_damage_forecast_cells.csv',index=False)
 pd.DataFrame([{'component':'construction pressure','status':'forecasted','meaning':'Dynamic World built-probability trend within 2 km; not probability of archaeological damage'},{'component':'quarry pressure','status':'unavailable','meaning':'quarry classifier has not passed required visual validation'},{'component':'damage outcome','status':'unavailable','meaning':'no longitudinal field-verified damage labels'}]).to_csv(out/'site_damage_forecast_scope.csv',index=False)
 z.to_csv(ROOT/'data/private/site_damage_forecast_private.csv',index=False)
if __name__=='__main__': main()
