from zo.aa.time import *


def test_calc_run_time():
    with calc_run_time():
        time.sleep(1)


def test_exec_time():
    @exec_time
    def sleep_1s():
        time.sleep(1)
    sleep_1s()
