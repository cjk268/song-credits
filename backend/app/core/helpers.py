from time import perf_counter
from functools import wraps

# Credit to https://superfastpython.com/asyncio-benchmark-decorator/
def benchmark(coro):
    @wraps(coro)
    async def wrapped(*args, **kwargs):
        time_start = perf_counter()
        try:
            return await coro(*args, **kwargs)
        finally:
            time_end = perf_counter()
            time_duration = time_end - time_start
            print(f'{coro.__name__} Took {time_duration:.3f} seconds')
    return wrapped