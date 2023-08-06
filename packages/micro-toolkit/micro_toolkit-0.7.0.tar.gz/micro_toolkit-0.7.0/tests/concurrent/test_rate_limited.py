import time
import timeit
import datetime
import concurrent.futures

from micro_toolkit.concurrent.rate_limited import rate_limited


def test_rate_limited():
    # test without rate limited
    def worker(x):
        time.sleep(0.9)
        return x

    start = timeit.default_timer()
    result = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Start the load operations and mark each future with its URL
        future_to_url = [executor.submit(worker, x) for x in range(10)]
        for future in concurrent.futures.as_completed(future_to_url):
            data = future.result()
            result.append(data)
    end = timeit.default_timer()

    expected = list(range(10))
    assert set(result) == set(expected)

    run_time = end - start
    assert datetime.timedelta(microseconds=900).seconds < run_time < datetime.timedelta(seconds=1).seconds

    # test with rate limited: type int
    @rate_limited(1)
    def rate_limited_worker(x):
        return x

    start = timeit.default_timer()
    result = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Start the load operations and mark each future with its URL
        future_to_url = [executor.submit(rate_limited_worker, x) for x in range(10)]
        for future in concurrent.futures.as_completed(future_to_url):
            data = future.result()
            result.append(data)
    end = timeit.default_timer()

    expected = list(range(10))
    assert set(result) == set(expected)

    run_time = end - start
    assert datetime.timedelta(seconds=11).seconds > run_time > datetime.timedelta(seconds=10).seconds

    # test with rate limited: type float
    @rate_limited(2.0)
    def rate_limited_worker(x):
        return x

    start = timeit.default_timer()
    result = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Start the load operations and mark each future with its URL
        future_to_url = [executor.submit(rate_limited_worker, x) for x in range(10)]
        for future in concurrent.futures.as_completed(future_to_url):
            data = future.result()
            result.append(data)
    end = timeit.default_timer()

    expected = list(range(10))
    assert set(result) == set(expected)

    run_time = end - start
    assert datetime.timedelta(seconds=6).seconds > run_time > datetime.timedelta(seconds=5).seconds
