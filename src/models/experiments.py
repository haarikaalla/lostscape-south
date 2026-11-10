"""Run reproducible PU, conformal, sanity-control and survey-efficiency experiments."""
from __future__ import annotations

from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import wilcoxon
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score

from src.eval.conformal import conformal_quantile,prediction_sets,empirical_coverage
from src.eval.metrics import ranking_metrics
from src.models.pu import PUBagging
from src.models.baselines import EXCLUDE

ROOT=Path(__file__).resolve().parents[2]
SEEDS=[11,29,47,71,101]

def calibrate(raw: np.ndarray,y: np.ndarray,apply: np.ndarray) -> np.ndarray:
    if np.unique(y).size<2: return apply
    z=np.clip(raw,1e-6,1-1e-6); a=np.log(z/(1-z)).reshape(-1,1)
    zz=np.clip(apply,1e-6,1-1e-6); b=np.log(zz/(1-zz)).reshape(-1,1)
    return LogisticRegression(C=1.0,max_iter=1000).fit(a,y).predict_proba(b)[:,1]

def main() -> None:
    d=pd.read_csv(ROOT/'data/private/model_table.csv')
    feats=[c for c in d.select_dtypes(include=np.number) if c not in EXCLUDE]
    rows=[]; conformal=[]; efficiency=[]; sanity=[]; predictions=[]
    for seed in SEEDS:
      rng=np.random.default_rng(seed)
      for held in sorted(d.feature_file.unique()):
        tr=d.feature_file.ne(held); te=~tr
        blocks=d.loc[tr,'spatial_block'].unique(); rng.shuffle(blocks)
        cal_blocks=set(blocks[:max(1,len(blocks)//5)])
        cal=tr & d.spatial_block.isin(cal_blocks); fit=tr & ~d.spatial_block.isin(cal_blocks)
        xfit=d.loc[fit,feats].to_numpy(); yfit=d.loc[fit,'label_positive'].to_numpy()
        xcal=d.loc[cal,feats].to_numpy(); ycal=d.loc[cal,'label_positive'].to_numpy()
        xt=d.loc[te,feats].to_numpy(); yt=d.loc[te,'label_positive'].to_numpy()
        model=PUBagging(estimators=10,unlabeled_ratio=5,seed=seed,trees_per_estimator=100).fit(xfit,yfit)
        pcal_raw=model.predict_proba(xcal)[:,1]; pt_raw=model.predict_proba(xt)[:,1]
        pt=calibrate(pcal_raw,ycal,pt_raw)
        unc=model.uncertainty(xt)
        rows.append({'seed':seed,'held_out':held,'model':'pu_bagging_calibrated',**ranking_metrics(yt,pt),'mean_uncertainty':float(unc.mean())})
        q=conformal_quantile(ycal,pcal_raw,.1); sets=prediction_sets(pt_raw,q)
        conformal.append({'seed':seed,'held_out':held,'alpha':.1,'nominal_coverage':.9,'empirical_coverage':empirical_coverage(yt,sets),'mean_set_size':sets.sum(1).mean(),'calibration_n':len(ycal),'calibration_positives':int(ycal.sum())})
        for budget in (1,2,5,10,20):
            k=max(1,int(np.ceil(len(yt)*budget/100))); order=np.argsort(-pt)[:k]
            efficiency.append({'seed':seed,'held_out':held,'strategy':'LostScape-PU','budget_pct':budget,'area_km2':k*25,'observed_sites':int(yt[order].sum()),'sites_per_100km2':float(yt[order].sum()/(k*25)*100)})
            rr=rng.choice(len(yt),size=k,replace=False)
            efficiency.append({'seed':seed,'held_out':held,'strategy':'random','budget_pct':budget,'area_km2':k*25,'observed_sites':int(yt[rr].sum()),'sites_per_100km2':float(yt[rr].sum()/(k*25)*100)})
        predictions.extend({'seed':seed,'held_out':held,'probability':float(p),'uncertainty':float(u),'label':int(y)} for p,u,y in zip(pt,unc,yt))
        ys=yfit.copy(); rng.shuffle(ys)
        sh=PUBagging(estimators=5,unlabeled_ratio=5,seed=seed,trees_per_estimator=50).fit(xfit,ys).predict_proba(xt)[:,1]
        sanity.append({'seed':seed,'held_out':held,'control':'shuffled_labels','pr_auc':average_precision_score(yt,sh),'positive_prevalence':float(yt.mean())})
    out=ROOT/'results/tables'; fig=ROOT/'results/figures'; out.mkdir(parents=True,exist_ok=True); fig.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(rows).to_csv(out/'lostscape_pu_spatial_cv.csv',index=False)
    pd.DataFrame(conformal).to_csv(out/'conformal_coverage.csv',index=False)
    pd.DataFrame(efficiency).to_csv(out/'survey_efficiency.csv',index=False)
    pd.DataFrame(sanity).to_csv(out/'sanity_checks.csv',index=False)
    pd.DataFrame(predictions).to_csv(ROOT/'data/private/predictions_private.csv',index=False)
    e=pd.DataFrame(efficiency).groupby(['strategy','budget_pct']).sites_per_100km2.agg(['mean','std']).reset_index()
    for s,g in e.groupby('strategy'): plt.plot(g.budget_pct,g['mean'],marker='o',label=s)
    plt.xlabel('Area budget (%)'); plt.ylabel('Observed sites per 100 km²'); plt.legend(); plt.tight_layout(); plt.savefig(fig/'survey_efficiency.png',dpi=300); plt.savefig(fig/'survey_efficiency.pdf'); plt.close()
    b=pd.read_csv(out/'baseline_spatial_cv.csv'); best=b.groupby('model').pr_auc.mean().idxmax(); bb=b[b.model.eq(best)].sort_values(['seed','held_out']).pr_auc.to_numpy(); pp=pd.DataFrame(rows).sort_values(['seed','held_out']).pr_auc.to_numpy()
    stat,p=wilcoxon(pp,bb,alternative='two-sided')
    pd.DataFrame([{'comparison':f'PU vs {best}','paired_runs':len(pp),'wilcoxon_statistic':stat,'p_value':p,'mean_difference':float(np.mean(pp-bb))}]).to_csv(out/'significance_tests.csv',index=False)
    print(json.dumps({'pu_runs':len(rows),'best_baseline':best,'wilcoxon_p':p},indent=2))

if __name__=='__main__': main()
