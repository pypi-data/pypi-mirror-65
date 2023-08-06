import threading
import time
from functools import wraps


class RateLimitedGroup:
    def __init__(self, max_per_second: float):
        self.max_per_second = max_per_second
        self.lock = threading.Lock()
        self.min_interval = 1.0 / max_per_second
        self.last_time_called = time.perf_counter()

    def __call__(self, func):
        @wraps(func)
        def rate_limited_function(*args, **kwargs):
            self.start()

            ret = func(*args, **kwargs)

            self.end()
            return ret

        return rate_limited_function

    def start(self):
        self.lock.acquire()
        elapsed = time.perf_counter() - self.last_time_called
        left_to_wait = self.min_interval - elapsed

        if left_to_wait > 0:
            time.sleep(left_to_wait)

    def end(self):
        self.last_time_called = time.perf_counter()
        self.lock.release()

    def __enter__(self):
        self.start()

    def __exit__(self, type, value, traceback):
        self.end()
