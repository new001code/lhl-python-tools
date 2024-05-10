from enum import Enum
from functools import wraps
from time import perf_counter_ns
from typing import Callable, Any, Union
from concurrent.futures import ThreadPoolExecutor
from lhltools import logger
from lhltools.async_tool import AsyncTool


class TimeRecorderTimeUnitEnum(Enum):
    MILLISECOND = 1000000
    SECOND = 1000000000
    MICROSECOND = 1000


class TimeRecorder(object):
    __slots__ = ["__unit", "__recorder", "__target_time", "__is_async"]

    @staticmethod
    def __default_recorder(desc, timeout, unit):
        logger.info(f"method:{desc}  -timeout:{timeout:.2f} {unit}")

    def __init__(
        self,
        recorder: Callable[..., Any] = __default_recorder,
        target_time: int = 0,
        is_async: bool = False,
        unit: TimeRecorderTimeUnitEnum = TimeRecorderTimeUnitEnum.MILLISECOND,
    ):
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
                    __async_tool = AsyncTool.get_instance()
                    if __async_tool is not None:
                        __default_process_pool = __async_tool.get_default_process_pool()
                        __default_process_pool.submit(
                            self.__recorder,
                            args=(
                                f"{func.__module__}.{func.__qualname__}",
                                float(timeout) / self.__unit.value,
                                self.__unit.name,
                            ),
                        )
                    else:
                        # 理论上不会执行到此处
                        logger.warning("async_tool is not initialized")
                else:
                    self.__recorder(
                        f"{func.__module__}.{func.__qualname__}.{func.__annotations__}",
                        float(timeout) / self.__unit.value,
                        self.__unit.name,
                    )
            return result

        return wrapper


class AsyncRun(object):

    __slots__ = ["__thread_pool"]
    __thread_pool: Union[ThreadPoolExecutor, str, None]

    def __init__(
        self,
        thread_pool: Union[ThreadPoolExecutor, str, None] = None,
    ):
        self.__thread_pool = thread_pool

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            async_tool = AsyncTool.get_instance()
            try:
                if self.__thread_pool is not None:
                    if isinstance(self.__thread_pool, str):
                        if async_tool is not None:
                            __pool = async_tool.get_thread_pool(self.__thread_pool)
                            __pool.submit(func, *args, **kwargs)
                    elif isinstance(self.__thread_pool, ThreadPoolExecutor):
                        self.__thread_pool.submit(func, *args, **kwargs)

                else:
                    if async_tool is not None:
                        __pool = async_tool.get_default_thread_pool()
                        __pool.submit(func, *args, **kwargs)
            except Exception as ex:
                logger.error(ex)

        return wrapper
