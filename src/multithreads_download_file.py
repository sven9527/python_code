"""
    多线程下载文件
"""
import threading, requests, time


class downloader:

    def __init__(self, url, thread_num, name):
        """
        初始化下载器
        :param url: 资源地址
        :param thread_num: 启动的线程数
        """
        if not url:
            print("url can't be None!")
            raise Exception
        self.num = thread_num
        self.url = url
        self.name = name
        # 获取文件大小
        r = requests.head(self.url)
        self.total = int(r.headers['Content-Length'])

    def get_range(self):
        """
        获取每个线程的下载区间
        :return:
        """
        ranges = []
        offset = int(self.total / self.num)
        for i in range(self.num):
            if i == self.num - 1:
                ranges.append((i * offset, self.total))
            else:
                ranges.append((i * offset, (i + 1) * offset))
        return ranges

    def download(self, start, end):
        """
        下载文件指定数据块
        :param start:
        :param end:
        :return:
        """
        headers = {'Range': 'Bytes=%s-%s' % (start, end), 'Accept-Encoding': '*'}
        res = requests.get(self.url, headers=headers)
        print('data {0}-{1} download success'.format(start, end))
        self.fd.seek(start)
        self.fd.write(res.content)

    def run(self):
        """
        启动下载
        :return:
        """
        self.fd = open(self.name, "wb")

        thread_list = []
        n = 0

        for ran in self.get_range():
            # 获取每个线程需要下载数据块
            start, end = ran
            n += 1
            thread = threading.Thread(target=self.download, args=(start, end))

            thread.start()
            thread_list.append(thread)

        for i in thread_list:
            i.join()

        self.fd.close()


if __name__ == "__main__":
    url = "https://wallpapersite.com/images/pages/pic_w/5537.jpg"
    url = "https://www.h2o.ai/wp-content/uploads/2018/01/Python-BOOKLET.pdf"
    name = 'Python-BOOKLET.pdf'
    num = 5
    now = lambda: time.time()
    start = now()
    print('start at : {}'.format(start))
    downloader(url, num, name).run()
    print('time passed {}'.format(now() - start))
