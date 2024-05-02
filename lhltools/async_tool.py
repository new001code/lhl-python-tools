class AsyncTool:
    """
    async tool
    """
    thread_pool_map = {},
    process_pool_map = {}

    def __init__(self):
        pass

    def __create_thread_pool(self, pool_name: str, max_workers: int = 10):
        """
        create thread pool
        """
        pass

    def __create_process_pool(self, pool_name: str, max_workers: int = 10):
        """
        create process pool
        """
        pass

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
