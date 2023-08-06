import sys
import time
import threading
from debugging import *
from omnitools import *


__ALL__ = ["Threadswrapper"]


class ThreadWrapper(object):
    total_thread_count = 0

    def __init__(self, semaphore: threading.Semaphore) -> None:
        self.threads = []
        self.sema = semaphore
        self.debug_time = False

    def __run_job(self, job: Callable[[Any], Any], args: tuple = None, result: list_or_dict = None,
                  key: Any = None) -> None:
        try:
            kwargs = args[1]
            args = args[0]
            start_time = time.time()
            self.total_thread_count += 1
            if isinstance(result, list):
                result += job(*args, **kwargs)
            elif isinstance(result, dict):
                result[key] = job(*args, **kwargs)
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
                    p(s)
        except:
            p(debug_info()[0])

    def add(self, job: Callable[[Any], Any], args: tuple = ((), {}), result: list_or_dict = None,
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


def args(*args, **kwargs):
    return args, kwargs


