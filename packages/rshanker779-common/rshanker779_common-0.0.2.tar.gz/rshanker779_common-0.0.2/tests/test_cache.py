import time

import rshanker779_common as utils


def test_cache():
    def expensive_fun():
        time.sleep(1)
        return 1

    start = time.time()
    cache = utils.Cache(utils.CachingStrategy("res", expensive_fun))
    end = time.time() - start
    assert end < 1
    # Has attr will call the cache, so need to make sure this section is timed

    start = time.time()
    assert hasattr(cache, "res")
    res = cache.res
    end = time.time() - start
    assert res == 1
    assert end > 1
    start = time.time()
    res = cache.res
    assert time.time() - start < 1


def test_multi_cache():
    def expensive_fun():
        time.sleep(0.5)
        return 1

    def expensive_fun_2():
        time.sleep(0.5)
        return 2

    start = time.time()
    cache = utils.Cache(
        utils.CachingStrategy("res1", expensive_fun),
        utils.CachingStrategy("res2", expensive_fun_2),
    )
    end = time.time() - start
    assert end < 0.5
    start = time.time()
    assert hasattr(cache, "res1")
    res1 = cache.res1
    assert res1 == 1
    assert hasattr(cache, "res2")
    res2 = cache.res2
    end = time.time() - start
    assert res2 == 2
    assert end > 1
