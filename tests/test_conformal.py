import numpy as np
from src.eval.conformal import conformal_quantile,empirical_coverage,prediction_sets


def test_conformal_shapes_and_coverage():
    y=np.array([0,0,1,1]); p=np.array([.05,.2,.8,.95])
    q=conformal_quantile(y,p,alpha=.25); sets=prediction_sets(p,q)
    assert sets.shape==(4,2)
    assert 0<=empirical_coverage(y,sets)<=1
