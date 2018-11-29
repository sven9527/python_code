import multiprocessing
from src.utils import time_record
import urllib.request

def func(msg):
    print('p_name: {0} - msg: {1}'.format(multiprocessing.current_process().name, msg))
    r = urllib.request.urlopen('https://www.baidu.com')
    return r.read()

@time_record
def eight_process_2_http():
    """
    8个进程，并发HTTP请求
    :return:
    """
    results = []
    pool = multiprocessing.Pool(processes=8)
    for i in range(10):
        msg = 'hello %d' % i
        # 异步进程池（异步指启动子进程的过程）
        results.append(pool.apply_async(func, (msg,)))
        # 同步进程池
        results.append(pool.apply(func, (msg,)))
    pool.close()
    pool.join()
    for r in results:
        res = r if not getattr(r, 'get', None) else r.get()
        print(res)

eight_process_2_http()