import numpy as np
from src.eval.metrics import expected_calibration_error,recall_at_area


def test_recall_at_area_perfect_ranking():
    y=np.array([1,0,0,0]); p=np.array([.9,.3,.2,.1])
    assert recall_at_area(y,p,.25)==1.0


def test_ece_perfect_probabilities():
    y=np.array([0,1]); p=np.array([0.,1.])
    assert expected_calibration_error(y,p)==0.0
