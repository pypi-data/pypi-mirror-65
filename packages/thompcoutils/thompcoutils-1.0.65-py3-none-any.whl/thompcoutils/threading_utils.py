import threading
import time
import datetime

_time_format = '%H:%M:%S'


def _test1(name, value1, value2):
    print("thread {} starting at {}".format(name, datetime.datetime.now().strftime(_time_format)))
    time.sleep(2)
    print("thread {} done at {}".format(name, datetime.datetime.now().strftime(_time_format)))
    value1 *= 5
    value2 *= 2
    return value1, value2


def _test2(name, value1):
    print("thread {} starting at {}".format(name, datetime.datetime.now().strftime(_time_format)))
    time.sleep(1)
    print("thread {} done at {}".format(name, datetime.datetime.now().strftime(_time_format)))
    value1 *= 3
    return value1


class ThreadManager (threading.Thread):
    THREAD_LOCK = threading.Lock()
    threads = {}

    def __init__(self, name, function, *argv):
        threading.Thread.__init__(self)
        self.name = name
        self.function = function
        self.args = argv
        self.rtn = None
        ThreadManager.threads[name] = self

    def run(self):
        self.rtn = self.function(*self.args)

    @staticmethod
    def start_all_threads():
        for thread_name in ThreadManager.threads:
            ThreadManager.threads[thread_name].start()

    @staticmethod
    def join_all_threads():
        for thread_name in ThreadManager.threads:
            ThreadManager.threads[thread_name].join()


def _main():
    # You can use the ThreadManager to take care of the threads for you:
    print('main starting at {}'.format(datetime.datetime.now().strftime(_time_format)))
    ThreadManager('one', _test1, 'one', 1, 2)
    ThreadManager('two', _test1, 'two', 3, 4)
    ThreadManager('three', _test2, 'three', 5)
    ThreadManager.start_all_threads()
    print('main starting work at {}'.format(datetime.datetime.now().strftime(_time_format)))
    time.sleep(1)
    print('main done working at {}'.format(datetime.datetime.now().strftime(_time_format)))
    ThreadManager.join_all_threads()

    for thread in ThreadManager.threads:
        print(ThreadManager.threads[thread].rtn)
    print("Back to Main Thread")

    # Or you can manage them yourself:
    thread1 = ThreadManager('one', _test1, 'one', 1, 2)
    thread2 = ThreadManager('two', _test1, 'two', 3, 4)
    thread3 = ThreadManager('three', _test2, 'three', 5)
    thread1.start()
    thread2.start()
    thread3.start()
    print('main starting work at {}'.format(datetime.datetime.now().strftime(_time_format)))
    time.sleep(1)
    print('main done working at {}'.format(datetime.datetime.now().strftime(_time_format)))
    thread1.join()
    thread2.join()
    thread3.join()
    print(thread1.rtn)
    print(thread2.rtn)
    print(thread3.rtn)
    print("Back to Main Thread")


if __name__ == '__main__':
    _main()
