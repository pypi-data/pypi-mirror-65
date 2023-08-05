import time
from contextlib import ContextDecorator
from loguru import logger as log


class calc_run_time(ContextDecorator):
    def __init__(self, name='run_time', base_time=0.000001):
        self.name = name
        self.base_time = base_time

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, *args):
        self.end = time.time()
        self.elapse = self.end - self.start
        if self.elapse > self.base_time:
            log.info(f"*** Processing time for {self.name} is: {self.elapse:.6f} seconds ***")


def exec_time(func):
    def new_func(*args, **args2):
        t1 = time.time()
        back = func(*args, **args2)
        t2 = time.time() - t1
        if t2 > 0.00001:
            log.info(f'{func.__name__} > take time: {t2:.6f}s')
        return back

    return new_func


def timestamp_str(n=0):  # 0 秒  3 毫秒  6 微秒
    return f'{10 ** n * time.time():.0f}'


def timestamp_int(n=0):  # 0 秒  3 毫秒  6 微秒
    return int(f'{10 ** n * time.time():.0f}')


def time_current(time_format='%Y-%m-%d %H:%M:%S'):
    return time.strftime(time_format)


def timestamp_to_format(aa, time_format='%Y-%m-%d %H:%M:%S'):  # %Y-%m-%d %H:%M:%S
    return time.strftime(time_format, time.localtime(aa))
