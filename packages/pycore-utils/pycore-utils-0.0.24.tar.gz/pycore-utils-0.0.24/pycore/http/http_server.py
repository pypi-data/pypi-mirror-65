# coding=utf-8
import socket
import threading
import traceback
from Queue import Queue

from pycore.http.handle import HttpRequest
from pycore.utils.logger_utils import LoggerUtils

logger = LoggerUtils('http_server').logger


class WorkThread(threading.Thread):
    def __init__(self, work_queue):
        super(WorkThread, self).__init__()
        self.work_queue = work_queue
        self.daemon = True

    def run(self):
        while True:
            func, args = self.work_queue.get()
            func(*args)
            self.work_queue.task_done()


# 线程池
class ThreadPoolManger:
    def __init__(self, thread_number):
        self.thread_number = thread_number
        self.work_queue = Queue()
        for i in range(self.thread_number):  # 生成一些线程来执行任务
            thread = WorkThread(self.work_queue)
            thread.start()

    def add_work(self, func, *args):
        self.work_queue.put((func, args))


def tcp_link(sock, addr, handle=HttpRequest):
    rfile = sock.makefile('rb', -1)
    http_req = handle(addr)
    try:
        http_req.passRequest(rfile)
    except:
        logger.exception(traceback.format_exc())
    sock.send(http_req.getResponse())
    sock.close()


def start_server(port, pool, handle=HttpRequest):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', port))
    s.listen(10)
    thread_pool = ThreadPoolManger(pool)
    while True:
        try:
            sock, addr = s.accept()
            thread_pool.add_work(tcp_link, *(sock, addr, handle))
        except:
            break
