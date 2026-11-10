"""Leakage-controlled spatial baseline runner."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier,RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from src.eval.metrics import ranking_metrics

ROOT=Path(__file__).resolve().parents[2]
EXCLUDE={"label_positive","latitude","longitude","distance_to_known_megalith_km","block_x","block_y","spatial_block","system:index",".geo","feature_file"}


def models(seed: int):
    return {
        "regularized_logistic":make_pipeline(SimpleImputer(),StandardScaler(),LogisticRegression(max_iter=2000,class_weight="balanced",random_state=seed)),
        "random_forest":make_pipeline(SimpleImputer(),RandomForestClassifier(n_estimators=500,min_samples_leaf=3,class_weight="balanced_subsample",n_jobs=-1,random_state=seed)),
        "hist_gradient_boosting":make_pipeline(SimpleImputer(),HistGradientBoostingClassifier(max_iter=300,l2_regularization=1.0,random_state=seed)),
    }


def main() -> None:
    data=pd.read_csv(ROOT/"data/private/model_table.csv")
    features=[c for c in data.select_dtypes(include=np.number).columns if c not in EXCLUDE]
    rows=[]
    for seed in [11,29,47,71,101]:
        for held_out in sorted(data.feature_file.unique()):
            train=data.feature_file.ne(held_out); test=~train
            if data.loc[train,"label_positive"].nunique()<2: continue
            for name,model in models(seed).items():
                model.fit(data.loc[train,features],data.loc[train,"label_positive"])
                p=model.predict_proba(data.loc[test,features])[:,1]
                rows.append({"seed":seed,"held_out":held_out,"model":name,**ranking_metrics(data.loc[test,"label_positive"].to_numpy(),p)})
    out=ROOT/"results/tables"; out.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(rows).to_csv(out/"baseline_spatial_cv.csv",index=False)
    print(json.dumps({"runs":len(rows),"features":features},indent=2))


if __name__=="__main__": main()

