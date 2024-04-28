import threading
from time import perf_counter_ns
from functools import wraps

__time_unit_map = {
    'ms': 1000000,
    's': 1000000000,
    'us': 1000,
    'ns': 1,
}


def __default_recorder(desc, timeout, unit):
    print(f"method:{desc}  -timeout:{timeout} {unit}")


def time_recorder(recorder=__default_recorder, targetTime=0, isAsync=False, unit='ms'):
    if not __time_unit_map.__contains__(unit.lower()):
        unit = "ms"
    ratio = __time_unit_map.__getitem__(unit.lower())

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            all_start_time = perf_counter_ns()
            result = func(*args, **kwargs)
            all_end_time = perf_counter_ns()

            timeout = all_end_time - all_start_time

            if timeout >= targetTime * ratio:
                if isAsync:
                    threading.Thread(target=recorder, args=(f"{func.__module__}.{func.__qualname__}",
                                                            float((all_end_time - all_start_time)) / ratio,
                                                            unit)).start()
                else:
                    recorder(
                        f"{func.__module__}.{func.__qualname__}",
                        float((all_end_time - all_start_time)) / ratio,
                        unit,
                        )
            return result

        return wrapper

    return decorator
