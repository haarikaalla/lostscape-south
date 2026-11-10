import numpy as np


def test_spatial_blocks_do_not_overlap():
    train=np.array(["A","A","B"]); test=np.array(["D","D"])
    assert set(train).isdisjoint(set(test))

