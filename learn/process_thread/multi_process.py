import multiprocessing
import threading
import time
import logging
import coloredlogs
import math

logger = logging.getLogger(__name__)
coloredlogs.install(level="DEBUG", logger=logger,
                    fmt='%(asctime)s %(processName)s.%(threadName)s.%(levelname)s: %(message)s')

cpu_count = multiprocessing.cpu_count()
tasks = range(0, 12)


def chunk(lst, n):
    list_len = len(lst)
    chunk_size = math.ceil(list_len / n)
    for i in range(0, list_len, chunk_size):
        yield lst[i:i + chunk_size]


def pro(tks, t_count):
    print(multiprocessing.current_process().name, len(tks))

    def sync_task():
        current_thread_name = threading.current_thread().getName()
        while True:
            if len(tks) == 0:
                break
            tk = tks.pop()
            logger.debug('current task: %s, current thread: %s' % (tk, current_thread_name))
            time.sleep(0.05)

    ts = []
    for i in range(0, t_count):
        t = threading.Thread(target=sync_task, name=f'Thread-{i}')
        t.start()
        ts.append(t)

    for t in ts:
        t.join()


thread_count = 10
ps = []
print(list(chunk(tasks, cpu_count)))

for t_chuck in list(chunk(tasks, cpu_count)):
    p = multiprocessing.Process(target=pro, args=(list(t_chuck), thread_count))
    p.start()
    ps.append(p)

for p in ps:
    p.join()

print(len(ps))
