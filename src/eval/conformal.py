"""Distribution-free split-conformal prediction sets for binary probabilities."""
from __future__ import annotations
import numpy as np


def conformal_quantile(y_cal: np.ndarray,p_cal: np.ndarray,alpha: float=.1) -> float:
    scores=np.where(y_cal==1,1-p_cal,p_cal)
    level=np.ceil((len(scores)+1)*(1-alpha))/len(scores)
    return float(np.quantile(scores,min(level,1.0),method="higher"))


def prediction_sets(p: np.ndarray,q: float) -> np.ndarray:
    include_zero=p<=q
    include_one=(1-p)<=q
    return np.c_[include_zero,include_one]


def empirical_coverage(y: np.ndarray,sets: np.ndarray) -> float:
    return float(np.mean(sets[np.arange(len(y)),y.astype(int)]))

