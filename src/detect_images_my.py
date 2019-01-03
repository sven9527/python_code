from multiprocessing.dummy import Process, Queue
import os, time, json
import requests
import gevent
import csv

# folder_path = '/home/zhangxing/Downloads/2018-12-5_8.3K/images/'
folder_path = '/home/zhangxing/Downloads/ticket-switch/test_case/'
detect_num_per_once = 3
timeout = 100
# service_url = "http://localhost:9090/check_ticket_switch"
service_url = "http://47.52.180.11/check_ticket_switch"
result_file = "my_ts_result_legacy_{0}.csv".format(time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime()))

result_q = Queue()


# Target:Store_Register_Year_Month_Day_Hour_Minute_Second.Millisecond_UPC.png
def detect_img(upc, img):
    files = {'search': open(folder_path + img, 'rb')}
    response = requests.post(service_url, data={'upc': upc, 'debug': 1}, files=files).json()
    return response


def output_result(n):
    results = []
    count = 0
    last_write_time = 0
    while True:
        try:
            r = result_q.get(block=False)
            results.append(r)
            if len(results) > n:
                with open(result_file, 'a') as f:
                    csv_writer = csv.writer(f)
                    while len(results) != 0:
                        item = results.pop()
                        csv_writer.writerow(item)
                        count += 1
                        print('now processed : ', count)
                last_write_time = time.time()
            if last_write_time != 0 and (time.time() - last_write_time) >= timeout:
                print('no more new message break')
                break
        except Exception as e:
            time.sleep(1)


def detect_once(imgs=None):
    tasks = []
    for t in imgs:
        upc = os.path.splitext(t)[0].split("_")[-1]
        tasks.append(gevent.spawn(detect_img, upc, t))
    try:
        gevent.joinall(tasks, raise_error=True)
    except Exception as e:
        gevent.kill(tasks[0])
        raise

    for index, img in enumerate(imgs):
        response = tasks[index].value
        filename = img
        upc = ''
        ticket_switch = ''
        detail = ''
        try:
            detail = json.dumps(response)
            upc = os.path.splitext(t)[0].split("_")[-1]
            ticket_switch = response['results'][0]["ticket_switch"]
            result_q.put(item=[1, filename, upc, ticket_switch, detail])
        except Exception as e:
            result_q.put(item=[0, filename, upc, ticket_switch, detail])
            print('Exception: ', e)


def go_detect(folder_path):
    """
    """
    imgs = []
    for root, dirs, files in os.walk(folder_path):
        for img in files:
            if len(imgs) >= detect_num_per_once:
                detect_once(imgs.copy())
                imgs = []
            imgs.append(img)
    if len(imgs) > 0:
        detect_once(imgs.copy())


if __name__ == '__main__':
    output_process = Process(target=output_result, args=(2,))
    output_process.start()

    go_detect(folder_path)

    output_process.join()
    print('Job Done!')
