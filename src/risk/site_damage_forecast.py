"""Benchmark and forecast construction pressure around known sites.

The target is five-year change in Dynamic World built probability within 2 km.
It is not an archaeological damage label.
"""
from __future__ import annotations
from pathlib import Path
import hashlib
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error,mean_squared_error

ROOT=Path(__file__).resolve().parents[2]
SEEDS=[11,29,47,71,101]

def cid(lat:float,lon:float)->str:
 return hashlib.sha256(f'LostScape-v1:{int(np.floor(lat/.09))}:{int(np.floor(lon/.09))}'.encode()).hexdigest()[:12]

def slope(v:np.ndarray)->float:
 return float(np.polyfit(np.arange(len(v),dtype=float),v,1)[0])

def theil_slope(v:np.ndarray)->float:
 return float(np.median([(v[j]-v[i])/(j-i) for i in range(len(v)) for j in range(i+1,len(v))]))

def features(w:pd.DataFrame,years:range)->pd.DataFrame:
 a=w[list(years)].to_numpy(float); x=pd.DataFrame(a,columns=[f'built_t{i}' for i in range(a.shape[1])],index=w.index)
 x['level_last']=a[:,-1]; x['mean']=a.mean(1); x['sd']=a.std(1); x['linear_slope']=[slope(v) for v in a]; x['robust_slope']=[theil_slope(v) for v in a]
 x['recent_minus_early']=a[:,-2:].mean(1)-a[:,:2].mean(1); x['acceleration']=(a[:,-1]-a[:,-2])-(a[:,1]-a[:,0])
 return pd.concat([x,pd.get_dummies(w.site_class,prefix='class',dtype=float)],axis=1)

def bootstrap_metric(y:np.ndarray,p:np.ndarray,fn,seed:int=20261110)->tuple[float,float]:
 rng=np.random.default_rng(seed); n=len(y); vals=[]
 for _ in range(1000):
  i=rng.integers(0,n,n); vals.append(fn(y[i],p[i]))
 return tuple(np.quantile(vals,[.025,.975]))

def metrics(y:np.ndarray,p:np.ndarray)->dict[str,float]:
 mae=mean_absolute_error(y,p); rmse=mean_squared_error(y,p)**.5; rho=0.0 if np.ptp(p)==0 else spearmanr(y,p).statistic
 k=max(1,int(np.ceil(.1*len(y)))); actual=set(np.argsort(-y)[:k]); predicted=set(np.argsort(-p)[:k]); top=len(actual&predicted)/k
 mlo,mhi=bootstrap_metric(y,p,mean_absolute_error); rlo,rhi=bootstrap_metric(y,p,lambda a,b:0.0 if np.ptp(b)==0 else np.nan_to_num(spearmanr(a,b).statistic))
 return {'mae':mae,'mae_ci95_low':mlo,'mae_ci95_high':mhi,'rmse':rmse,'spearman':rho,'spearman_ci95_low':rlo,'spearman_ci95_high':rhi,'top_decile_recall':top}

def main()->None:
 raw=pd.read_csv(ROOT/'data/private/site_damage_history_2016_2025.csv'); meta=raw.groupby('site_key').agg(state=('state','first'),site_class=('site_class','first'))
 w=raw.pivot(index='site_key',columns='year',values='built_probability').join(meta).dropna().reset_index(); x=features(w,range(2016,2021)); y=(w[2025]-w[2020]).to_numpy(float)
 rows=[]; preds=[]; states=sorted(w.state.unique())
 for held in states:
  test=w.state.eq(held).to_numpy(); remaining=[s for s in states if s!=held]; cal_state=max(remaining,key=lambda s:int(w.state.eq(s).sum())); cal=w.state.eq(cal_state).to_numpy(); fit=~test&~cal
  baselines={'persistence':np.zeros(test.sum()),'linear_trend':x.loc[test,'linear_slope'].to_numpy()*5,'robust_theil_sen':x.loc[test,'robust_slope'].to_numpy()*5}
  for name,p in baselines.items(): rows.append({'held_out_state':held,'calibration_state':'none','model':name,'n_test':int(test.sum()),**metrics(y[test],p),'interval_coverage_90':np.nan,'mean_interval_width':np.nan})
  seed_predictions=[]
  for seed in SEEDS:
   model=HistGradientBoostingRegressor(max_iter=200,l2_regularization=1.0,max_leaf_nodes=15,min_samples_leaf=20,random_state=seed).fit(x.loc[fit],y[fit]); seed_predictions.append(model.predict(x.loc[test]))
  p=np.mean(seed_predictions,axis=0)
  cal_model=HistGradientBoostingRegressor(max_iter=200,l2_regularization=1.0,max_leaf_nodes=15,min_samples_leaf=20,random_state=20261110).fit(x.loc[fit],y[fit]); cres=np.abs(y[cal]-cal_model.predict(x.loc[cal])); q=float(np.quantile(cres,min(1,np.ceil((len(cres)+1)*.9)/len(cres)),method='higher'))
  rows.append({'held_out_state':held,'calibration_state':cal_state,'model':'hgb_temporal_context','n_test':int(test.sum()),**metrics(y[test],p),'interval_coverage_90':float(np.mean((y[test]>=p-q)&(y[test]<=p+q))),'mean_interval_width':2*q})
  for key,yy,pp,lo,hi in zip(w.loc[test,'site_key'],y[test],p,p-q,p+q): preds.append({'site_key':key,'state':held,'observed_change_2020_2025':yy,'predicted_change_2020_2025':pp,'prediction_low_90':lo,'prediction_high_90':hi})
 table=pd.DataFrame(rows); out=ROOT/'results/tables'; table.to_csv(out/'site_damage_forecast_model_comparison.csv',index=False)
 weighted_mae=table.groupby('model').apply(lambda g:np.average(g.mae,weights=g.n_test),include_groups=False)
 weighted_top=table.groupby('model').apply(lambda g:np.average(g.top_decile_recall,weights=g.n_test),include_groups=False)
 # The operational task is prioritization, so selection is fixed to top-decile recall,
 # not post-hoc magnitude fit. MAE is reported separately and may favor persistence.
 chosen=weighted_top.idxmax()
 latest=features(w,range(2021,2026)).reindex(columns=x.columns,fill_value=0); ensemble=[]
 if chosen=='hgb_temporal_context':
  for seed in SEEDS: ensemble.append(HistGradientBoostingRegressor(max_iter=200,l2_regularization=1.0,max_leaf_nodes=15,min_samples_leaf=20,random_state=seed).fit(x,y).predict(latest))
  delta=np.mean(ensemble,axis=0); epistemic=np.std(ensemble,axis=0,ddof=1)
 elif chosen=='linear_trend': delta=latest.linear_slope.to_numpy()*5; epistemic=np.zeros(len(w))
 elif chosen=='robust_theil_sen': delta=latest.robust_slope.to_numpy()*5; epistemic=np.zeros(len(w))
 else: delta=np.zeros(len(w)); epistemic=np.zeros(len(w))
 if chosen=='linear_trend': chosen_backtest=x.linear_slope.to_numpy()*5
 elif chosen=='robust_theil_sen': chosen_backtest=x.robust_slope.to_numpy()*5
 elif chosen=='persistence': chosen_backtest=np.zeros(len(y))
 else:
  pv=pd.DataFrame(preds).set_index('site_key'); chosen_backtest=w.site_key.map(pv.predicted_change_2020_2025).to_numpy()
 q_global=float(np.quantile(np.abs(y-chosen_backtest),.9,method='higher'))
 inv=pd.read_csv(ROOT/'data/private/master_inventory_precise.csv').dropna(subset=['lat','lon']); inv['site_key']=[hashlib.sha256(f'{a}:{b}'.encode()).hexdigest()[:16] for a,b in zip(inv.source,inv.source_id)]; inv['cell_id_10km']=[cid(a,b) for a,b in zip(inv.lat,inv.lon)]
 z=w[['site_key','state',2025]].rename(columns={2025:'built_2025'}).copy(); z['model_selected']=chosen; z['projected_change_2025_2030']=delta; z['change_low_90']=delta-q_global; z['change_high_90']=delta+q_global; z['forecast_built_2030']=np.clip(z.built_2025+delta,0,1); z['ensemble_sd']=epistemic; z=z.merge(inv[['site_key','cell_id_10km']],on='site_key',how='left')
 cell=z.groupby(['state','cell_id_10km','model_selected'],as_index=False).agg(site_count=('site_key','nunique'),built_2025=('built_2025','mean'),forecast_built_2030=('forecast_built_2030','mean'),projected_change_2025_2030=('projected_change_2025_2030','mean'),change_low_90=('change_low_90','mean'),change_high_90=('change_high_90','mean'),ensemble_sd=('ensemble_sd','mean'))
 cell['forecast_pressure_score']=cell.projected_change_2025_2030
 cell.sort_values(['state','forecast_pressure_score'],ascending=[True,False]).groupby('state').head(50).to_csv(out/'site_damage_forecast_cells.csv',index=False)
 pd.DataFrame([{'selection_objective':'rank future pressure growth','selected_model':chosen,'selection_metric':'weighted state-holdout top-decile recall','selected_value':weighted_top[chosen],'best_mae_model':weighted_mae.idxmin(),'best_mae':weighted_mae.min(),'interpretation':'ranking screen only; exact magnitude forecast has no demonstrated skill over persistence'}]).to_csv(out/'site_damage_forecast_selection.csv',index=False)
 pd.DataFrame([{'component':'construction pressure','status':'weak ranking forecast','meaning':'Dynamic World built-probability change within 2 km; model selected by state-holdout top-decile recall'},{'component':'2035 construction pressure','status':'not released','meaning':'ten-year recursive extrapolation was not supported by the five-year backtest'},{'component':'quarry pressure','status':'unavailable','meaning':'quarry classifier has not passed required visual validation'},{'component':'damage outcome','status':'unavailable','meaning':'no longitudinal field-verified damage labels'}]).to_csv(out/'site_damage_forecast_scope.csv',index=False)
 pd.DataFrame(preds).to_csv(ROOT/'data/private/site_damage_backtest_predictions_private.csv',index=False); z.to_csv(ROOT/'data/private/site_damage_forecast_private.csv',index=False)
 print({'selected_model':chosen,'sites':len(w),'global_90pct_residual':q_global,'weighted_mae':weighted_mae.to_dict(),'weighted_top_decile_recall':weighted_top.to_dict()})
if __name__=='__main__': main()
