
from random import randint
from threading import Thread
from time import time, sleep


class DownloadTask(Thread):
    def __init__(self, filename):
        super().__init__()
        self._filename = filename

    def run(self):
        print('Start downloading %s...' % self._filename)
        time_to_download = randint(3, 5)
        sleep(time_to_download)
        print('%s download completed! Cost %ss' % (self._filename, time_to_download))


def main():
    start = time()
    t1 = DownloadTask('Python_Learn.pdf')
    t1.start()

    t2 = DownloadTask('Shenzhen Hot.mkv')
    t2.start()

    # 阻塞线程，等待执行完成
    t1.join()
    t2.join()

    end = time()
    print('Total cost %.2fs' % (end - start))


if __name__ == '__main__':
    main()
