import os
import requests
import json
import csv
import logging
from multiprocessing.dummy import Pool, Queue, Process
import time

image_root_path = '/home/zhangxing/Downloads/2018-12-5_8.3K/images/'
# service_url = "http://47.52.180.11/check_ticket_switch"
service_url = "http://localhost:9090/check_ticket_switch"
result_file = "output/ts_result_legacy_{0}.csv".format(time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime()))

logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)


result_q = Queue()


def call_service(image_local_path):
    file_name = os.path.split(image_local_path)[-1]
    upc = ""
    ticket_switch = ""
    detail = ""
    try:
        files = {"search": open(image_local_path, 'rb')}
        upc = os.path.splitext(image_local_path)[0].split("_")[-1]
        response = requests.post(service_url, data = {"upc":upc, "debug":1}, files=files).json()
        detail = json.dumps(response)
        ticket_switch = response["results"][0]["ticket_switch"]
        result_q.put(item = [1, file_name, upc, ticket_switch, detail])

    except Exception as e:
        logger.exception("Failed to process image {0}".format(file_name))
        result_q.put(item = [0, file_name, upc, ticket_switch, detail])


def ouput_result(n):
    results = []
    count = 0
    last_write_time = 0
    while 1:
        try:
            r = result_q.get(block=False)
            results.append(r)
            if len(results)>=n:
                with open(result_file, "a") as f:
                    csv_writer = csv.writer(f)
                    for item in results:
                        csv_writer.writerow(item)
                        logger.debug(item)
                        count+=1
                        if count % 10==0:
                            logger.info(count)
                    last_write_time = time.time()
                results = []
            if last_write_time != 0 and (time.time() - last_write_time) > 1200:
                logger.info("long time on data")
                break
        except Exception:
            time.sleep(1)


def select_ts_img(is_ticket_switch):
    """
    从指定csv中读取指定图片做detect
    :return:
    """
    flag = 1 if is_ticket_switch else 0
    result_file_path = "output/ts_result_legacy_2018-12-11_10:42:58.csv"
    none_ts_imgs = []
    with open(result_file_path) as f:
        csv_reader = csv.reader(f)
        for item in csv_reader:
            success = int(item[0])
            ticket_switch = -1 if item[3] == '' else int(item[3])
            if success == 1 and ticket_switch == flag:
                none_ts_imgs.append(image_root_path + item[1])
    return none_ts_imgs


if __name__ == "__main__":
    # image_path_list = [os.path.join(image_root_path, x) for x in os.listdir(image_root_path)]
    # logger.info(len(image_path_list))

    # image_path_list = select_ts_img(False)
    image_path_list = select_ts_img(True)
    logger.info(len(image_path_list))

    output_process = Process(target=ouput_result, args=(2,))
    output_process.start()

    pool = Pool(10)
    pool.map(call_service, image_path_list)
    pool.close()
    pool.join()

    output_process.join()
    logger.info("Done!")
