import time


now = lambda: time.time()

def time_record(func, time_key=None):
    time_key = time_key if time_key else func.__name__

    def wrapper(*args, **kwargs):
        start = now()
        func_ret = func(*args, **kwargs)
        end = now()
        print('{0} ends, time elapse: {1}'.format(time_key, end - start))
        return func_ret

    return wrapper