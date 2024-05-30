import time


class Ts_time():
    def Times(self):
        ts = int(time.time() * 1000)
        print("ts_time is :", ts)
        return ts