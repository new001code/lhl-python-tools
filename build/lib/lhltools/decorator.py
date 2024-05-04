from enum import Enum
from functools import wraps
from threading import Thread
from time import perf_counter_ns
from typing import Callable, Any
from lhltools import logger


class TimeRecorderTimeUnitEnum(Enum):
    MILLISECOND = 1000000
    SECOND = 1000000000
    MICROSECOND = 1000


__async_type = ("thread", "process", "aio")


class TimeRecorder(object):
    __slots__ = ['__unit', '__recorder', '__target_time', '__is_async']

    @staticmethod
    def __default_recorder(desc, timeout, unit):
        logger.info(f"method:{desc}  -timeout:{timeout:.2f} {unit}")

    def __init__(self, recorder: Callable[..., Any] = __default_recorder, target_time: int = 0, is_async: bool = False,
                 unit: TimeRecorderTimeUnitEnum = TimeRecorderTimeUnitEnum.MILLISECOND):
        self.__unit = unit
        self.__recorder = recorder
        self.__target_time = target_time
        self.__is_async = is_async

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            all_start_time = perf_counter_ns()
            result = func(*args, **kwargs)
            all_end_time = perf_counter_ns()
            timeout = all_end_time - all_start_time
            if timeout >= self.__target_time * self.__unit.value:
                if self.__is_async:
                    Thread(
                        target=self.__recorder,
                        args=(
                            f"{func.__module__}.{func.__qualname__}",
                            float(timeout) / self.__unit.value,
                            self.__unit.name,
                        ),
                    ).start()
                else:
                    self.__recorder(
                        f"{func.__module__}.{func.__qualname__}.{func.__annotations__}",
                        float(timeout) / self.__unit.value,
                        self.__unit.name)
            return result

        return wrapper
