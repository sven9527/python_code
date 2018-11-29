import asyncio, time

now = lambda: time.time()


async def do_some_work(param):
    print('waiting step one: {}'.format(param))
    await asyncio.sleep(3)
    print('continue: {}'.format(param))
    return 'Done'


def callback(future):
    print('callback {}'.format(future.result()))


async def main():
    loop = asyncio.get_event_loop()
    tasks = []
    task1 = loop.create_task(do_some_work(1))
    task2 = asyncio.ensure_future(do_some_work(2))
    task2.add_done_callback(callback)
    tasks.append(task1)
    tasks.append(task2)
    for i in range(100):
        tasks.append(loop.create_task(do_some_work(i + 100)))
    # print(tasks)
    return await asyncio.wait(tasks)


# 协程嵌套
start = now()
loop = asyncio.get_event_loop()
done, pending = loop.run_until_complete(main())
for d in done:
    print(d)
print('TIME: {}'.format(now() - start))
