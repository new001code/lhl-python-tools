import threading
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
from typing import Any,Dict

class AsyncTool(object):
    """
    async tool
    """
    __thread_pool_map:Dict[str, Any] = {}
    __process_pool_map:Dict[str, Any] = {}

    _single_lock = threading.RLock()


    @classmethod
    def get_instance(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with AsyncTool._single_lock:
                if not hasattr(cls, "_instance"):
                    AsyncTool._instance =AsyncTool(*args, **kwargs)
        return cls._instance

    def __create_thread_pool(self, pool_name: str, max_workers: int = 10):
        """
        create thread pool
        """
        if pool_name not in AsyncTool.__thread_pool_map:
            with AsyncTool._single_lock:
                if pool_name not in AsyncTool.__thread_pool_map:
                    self.__thread_pool_map[pool_name] = ThreadPoolExecutor(max_workers=max_workers)

        return self.__thread_pool_map[pool_name]

    def __create_process_pool(self, pool_name: str, max_workers: int = 10):
        """
        create process pool
        """
        if pool_name not in AsyncTool.__process_pool_map:
            with AsyncTool._single_lock:
                if pool_name not in AsyncTool.__process_pool_map:
                    AsyncTool.__process_pool_map[pool_name] = ProcessPoolExecutor(max_workers=max_workers)

        return self.__process_pool_map[pool_name]

    def get_thread_pool(self, pool_name: str):
        """
        get thread pool
        """
        pass




    def get_process_pool(self, pool_name: str):
        """
        get process pool
        """
        pass
    

    def get_default_thread_pool(self):
        default_pool = self.__create_thread_pool("default")
        print(type(default_pool))
        return self.__create_thread_pool("default")

    def get_default_process_pool(self):
        return self.__create_process_pool("default")
