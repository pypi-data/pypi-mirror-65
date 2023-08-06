from . import *


def main():
    def a(b, c=None):
        return f"{b}, {c}"
    tw = ThreadWrapper(threading.Semaphore(1))
    result = {}
    for i in range(10):
        tw.add(job=a, result=result, key=i, args=args(i**2, c=i**3))
    tw.wait()
    print(result)


if __name__ == "__main__":
    main()
