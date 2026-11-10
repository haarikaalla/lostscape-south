import numpy as np
from sklearn.metrics import average_precision_score, roc_auc_score


def test_metric_sanity():
    y=np.array([0,0,1,1]); good=np.array([0.1,0.2,0.8,0.9]); bad=1-good
    assert roc_auc_score(y,good)==1.0
    assert average_precision_score(y,good)>average_precision_score(y,bad)

