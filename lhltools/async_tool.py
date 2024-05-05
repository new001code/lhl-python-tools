import threading
import os
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import Dict
from lhltools import thread_pool_conf_map, process_pool_conf_map


class ThreadPoolNotFoundException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class ProcessPoolNotFoundException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class AsyncTool(object):
    """
    async tool
    """

    __instance = None
    __thread_pool_map: Dict[str, ThreadPoolExecutor] = {}
    __process_pool_map: Dict[str, ProcessPoolExecutor] = {}

    _single_lock = threading.RLock()

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(AsyncTool, cls).__new__(cls)
        return cls.__instance

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, "__instance"):
            with AsyncTool._single_lock:
                if not hasattr(cls, "__instance"):
                    AsyncTool.__instance = AsyncTool()
        return AsyncTool.__instance

    def __create_thread_pool(self, pool_name: str, max_workers: int = 10):
        """
        create thread pool
        """
        if pool_name not in AsyncTool.__thread_pool_map:
            with AsyncTool._single_lock:
                if pool_name not in AsyncTool.__thread_pool_map:
                    self.__thread_pool_map[pool_name] = ThreadPoolExecutor(
                        max_workers=max_workers
                    )

        return self.__thread_pool_map[pool_name]

    def __create_process_pool(self, pool_name: str, max_workers: int):
        """
        create process pool
        """
        if pool_name not in AsyncTool.__process_pool_map:
            with AsyncTool._single_lock:
                if pool_name not in AsyncTool.__process_pool_map:
                    AsyncTool.__process_pool_map[pool_name] = ProcessPoolExecutor(
                        max_workers=max_workers
                    )

        return self.__process_pool_map[pool_name]

    def get_thread_pool(self, pool_name: str) -> ThreadPoolExecutor:
        """
        get thread pool
        """
        if pool_name not in self.__thread_pool_map:
            raise ThreadPoolNotFoundException(f"thread pool {pool_name} not found")
        elif (
            pool_name not in self.__thread_pool_map
            and pool_name in thread_pool_conf_map
        ):
            return self.__create_thread_pool(pool_name, thread_pool_conf_map[pool_name])
        else:
            return self.__thread_pool_map[pool_name]

    def get_process_pool(self, pool_name: str) -> ProcessPoolExecutor:
        """
        get process pool
        """
        if (
            pool_name not in self.__process_pool_map
            and pool_name not in process_pool_conf_map
        ):
            raise ProcessPoolNotFoundException(f"process pool {pool_name} not found")
        elif (
            pool_name not in self.__process_pool_map
            and pool_name in process_pool_conf_map
        ):
            return self.__create_process_pool(
                pool_name, process_pool_conf_map[pool_name]
            )
        else:
            return self.__process_pool_map[pool_name]

    def get_default_thread_pool(self) -> ThreadPoolExecutor:
        return self.__create_thread_pool("default")

    def get_default_process_pool(self) -> ProcessPoolExecutor:
        return self.__create_process_pool("default", os.cpu_count() or 1)
