from threading import Timer
from datetime import datetime
import time


# 使用Timer实现定时任务
def timer_task(task_id):
    Timer(1, task, (task_id,)).start()


def task(task_id):
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '{} is finished'.format(task_id))


# 使用sched
import sched


def timer_sched_task(task_id):
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(1, 1, task, (task_id,))
    scheduler.enter(1, 1, task, (task_id,))
    scheduler.run()




if __name__ == "__main__":
    task_id = 0
    while True:
        task_id += 1
        # timer_task(task_id)
        timer_sched_task(task_id)
        print(time.time())
        time.sleep(5)
