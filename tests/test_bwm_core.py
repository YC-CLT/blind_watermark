import numpy as np
from blind_watermark.bwm_core import (
    one_dim_kmeans,
    random_strategy1,
    random_strategy2,
)


def test_one_dim_kmeans_binary():
    inputs = np.array([0.1, 0.9, 0.2, 0.8, 0.15, 0.85])
    result = one_dim_kmeans(inputs)
    assert result.dtype == bool
    assert 1 <= result.sum() <= len(result) - 1


def test_one_dim_kmeans_convergence():
    inputs = np.array([0.01, 0.02, 0.99, 0.98, 0.01, 0.99])
    result = one_dim_kmeans(inputs)
    assert not result[0]
    assert not result[1]
    assert result[2]
    assert result[3]


def test_random_strategy1_shape():
    result = random_strategy1(seed=42, size=10, block_shape=16)
    assert result.shape == (10, 16)


def test_random_strategy_deterministic():
    a1 = random_strategy1(seed=42, size=5, block_shape=16)
    a2 = random_strategy1(seed=42, size=5, block_shape=16)
    assert np.array_equal(a1, a2)


def test_random_strategy_different_seeds():
    a1 = random_strategy1(seed=1, size=5, block_shape=16)
    a2 = random_strategy1(seed=2, size=5, block_shape=16)
    assert not np.array_equal(a1, a2)


def test_random_strategy2():
    result = random_strategy2(seed=42, size=10, block_shape=16)
    assert result.shape == (10, 16)
    for i in range(1, len(result)):
        assert np.array_equal(result[0], result[i])