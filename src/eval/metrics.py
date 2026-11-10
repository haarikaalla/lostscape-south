"""Metrics for spatial ranking, calibration, and PU evaluation."""
from __future__ import annotations

import numpy as np
from sklearn.metrics import average_precision_score, roc_auc_score


def expected_calibration_error(y: np.ndarray,p: np.ndarray,bins: int=10) -> float:
    edges=np.linspace(0,1,bins+1); total=len(y); score=0.0
    for lo,hi in zip(edges[:-1],edges[1:]):
        mask=(p>=lo)&(p<(hi if hi<1 else hi+1e-12))
        if mask.any(): score+=mask.sum()/total*abs(y[mask].mean()-p[mask].mean())
    return float(score)


def recall_at_area(y: np.ndarray,p: np.ndarray,fraction: float) -> float:
    k=max(1,int(np.ceil(len(y)*fraction))); chosen=np.argsort(-p)[:k]
    positives=y.sum()
    return float(y[chosen].sum()/positives) if positives else float("nan")


def ranking_metrics(y: np.ndarray,p: np.ndarray) -> dict[str,float]:
    out={"pr_auc":float(average_precision_score(y,p)),"ece":expected_calibration_error(y,p)}
    out["roc_auc"]=float(roc_auc_score(y,p)) if np.unique(y).size==2 else float("nan")
    for pct in (1,5,10,20): out[f"recall_top_{pct}pct"]=recall_at_area(y,p,pct/100)
    # In PU evaluation this is observed-positive recall, explicitly not population recall.
    out["pu_observed_positive_mean_rank"]=float(np.mean(np.argsort(np.argsort(-p))[y==1])+1) if y.sum() else float("nan")
    return out

