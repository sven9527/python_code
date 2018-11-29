import time, gevent
import gevent.monkey
import urllib.request

# monkey patch
gevent.monkey.patch_socket()

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


@time_record
def f1(num=0):
    print('1 started polling: {}'.format(now()))
    gevent.sleep(num)
    print('1 ended ppolling: {}'.format(now()))


@time_record
def f2(num=0):
    print('2 started polling: {}'.format(now()))
    gevent.sleep(num)
    print('2 ended ppolling: {}'.format(now()))


# gevent.joinall([
#     gevent.spawn(f1, num=1),
#     gevent.spawn(f2, num=2),
# ])


def task():
    gevent.sleep(0.02)


@time_record
def synchronous():
    for i in range(1, 10):
        task()


@time_record
def asynchronous():
    tasks = [gevent.spawn(task, i) for i in range(1, 10)]
    gevent.joinall(tasks)


# print(synchronous.__name__, ': ----->')
# synchronous()
#
# print(asynchronous.__name__, ': ------>')
# asynchronous()


# ==================asynchronous http test====================================
def fetch():
    resp = urllib.request.urlopen('http://www.baidu.com')
    html = resp.read()


@time_record
def synchronous():
    for i in range(1, 10):
        fetch()


@time_record
def asynchronous():
    tasks = [gevent.spawn(fetch) for i in range(1, 10)]
    gevent.joinall(tasks)


print(synchronous.__name__, ': ----->')
synchronous()

print(asynchronous.__name__, ': ------>')
asynchronous()

# ============= create greenlet ==========================
from gevent import Greenlet


def foo(msg, n):
    gevent.sleep(n)
    print(msg, n)

def fail(n):
    print('fail')

t1 = Greenlet.spawn(foo, 'Hello', 1)
t2 = gevent.spawn(foo, 'i live!', 2)
t3 = gevent.spawn(fail, 1)

ts = [t1, t2, t3]
# 协程状态
print(t3.started)
try:
    gevent.joinall(ts)
except Exception as e:
    print(e)
finally:
    print('done')
print(t3.ready())
print(t3.successful())
print(t3.exception)



from gevent import Timeout

# 设置超时
try:
    with Timeout(2):
        gevent.sleep(3)
except Timeout:
    print('timeout')
