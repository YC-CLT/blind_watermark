from blind_watermark.pool import CommonPool, AutoPool


def test_common_pool_map():
    pool = CommonPool()
    result = pool.map(lambda x: x * 2, [1, 2, 3])
    assert result == [2, 4, 6]


def test_auto_pool_common_mode():
    pool = AutoPool(mode="common", processes=None)
    result = pool.map(lambda x: x + 1, [1, 2, 3])
    assert result == [2, 3, 4]


def test_auto_pool_unknown_mode_falls_back():
    pool = AutoPool(mode="nonexistent", processes=None)
    result = pool.map(str, [1, 2])
    assert result == ["1", "2"]