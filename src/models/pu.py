"""Positive-unlabeled bagging with out-of-bag uncertainty."""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np
from sklearn.base import clone
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer


@dataclass
class PUBagging:
    estimators: int=25
    unlabeled_ratio: int=5
    seed: int=20261110

    def fit(self,x: np.ndarray,y: np.ndarray):
        self.imputer_=SimpleImputer().fit(x); z=self.imputer_.transform(x)
        pos=np.flatnonzero(y==1); unl=np.flatnonzero(y==0)
        if not len(pos): raise ValueError("PU learning requires observed positives")
        rng=np.random.default_rng(self.seed); self.models_=[]
        for i in range(self.estimators):
            sample=rng.choice(unl,size=min(len(unl),self.unlabeled_ratio*len(pos)),replace=False)
            idx=np.r_[pos,sample]; target=np.r_[np.ones(len(pos)),np.zeros(len(sample))]
            model=RandomForestClassifier(n_estimators=250,min_samples_leaf=3,class_weight="balanced",n_jobs=-1,random_state=self.seed+i)
            model.fit(z[idx],target); self.models_.append(model)
        return self

    def predict_distribution(self,x: np.ndarray) -> np.ndarray:
        z=self.imputer_.transform(x)
        return np.vstack([m.predict_proba(z)[:,1] for m in self.models_])

    def predict_proba(self,x: np.ndarray) -> np.ndarray:
        p=self.predict_distribution(x).mean(axis=0)
        return np.c_[1-p,p]

    def uncertainty(self,x: np.ndarray) -> np.ndarray:
        return self.predict_distribution(x).std(axis=0,ddof=1)

