import sys
import time
import threading
from typing import *
from debugging import *


__ALL__ = ["Threadswrapper"]


list_or_dict = Union[list, dict]


class ThreadWrapper(object):
    total_thread_count = 0

    def __init__(self) -> None:
        self.threads = []
        self.debug_time = False

    def __run_job(self, job: Callable[[Any], Any], args: Tuple = None, result: list_or_dict = None,
                  key: Any = None) -> None:
        start_time = time.time()
        self.total_thread_count += 1
        try:
            if isinstance(result, list):
                result += job(*args)
            elif isinstance(result, dict):
                result[key] = job(*args)
        except:
            print(debug_info()[0], flush=True)
        duration = time.time()-start_time
        if self.debug_time:
            count = str(self.total_thread_count).ljust(20)
            qualname = job.__qualname__.ljust(50)
            timestamp = str(int(time.time() * 1000) / 1000).ljust(20)[6:]
            s = f"Thread {count}{qualname}{timestamp}{duration}s\n"
            if duration >= 0.5:
                sys.stderr.write(s)
                sys.stderr.flush()
            else:
                sys.stdout.write(s)
                sys.stdout.flush()

    def add(self, job: Callable[[Any], Any], args: Tuple = (), result: list_or_dict = None,
            key: Any = None) -> bool:
        if result is None:
            result = {}
        if key is None:
            key = 0
        thread = threading.Thread(target=self.__run_job, args=(job, args, result, key))
        self.threads.append(thread)
        thread.start()
        return True

    def wait(self) -> bool:
        for thread in self.threads:
            thread.join()
        return True


