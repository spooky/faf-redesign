import time
import logging
from tasks import uitask, Indefinite, Progressive, progress


def callback(result):
    logger = logging.getLogger(__name__)
    logger.debug('callback result: {}'.format(result))


@uitask(Indefinite, finished=callback)
def long_operation():
    time.sleep(3)
    return 'a'
long_operation.description = 'running without reporting progress'


@uitask(Progressive, finished=callback)
def long_operation_with_progress():
    count = 0
    while count < 10:
        time.sleep(0.3)
        progress((count+1), 10)
        count += 1
    return 'b'
long_operation_with_progress.description = 'running and reporting progress'


@uitask(Progressive, finished=callback)
def long_operation_with_arguments(p1):
    count = 0
    while count < 10:
        time.sleep(0.3)
        progress((count+1), 10)
        count += 1
    return 'b'
long_operation_with_arguments.description = 'running with an argument and reporting progress'


class Downloader:
    def __init__(self, url):
        self.url = url

    # def callback(self, result):
    #     logger = logging.getLogger(__name__)
    #     logger.debug('downloader callback result: {}'.format(result))

    @uitask(Progressive)
    def run(self):
        for i in range(0,10):
            time.sleep(0.3)
            progress((i+1)/10)

        return self.url
    run.description = 'downloading with run' # property(str, lambda self: 'downloading {}'.format(self.url))

    @uitask(Progressive)
    def run2(self, p1):
        for i in range(0,10):
            time.sleep(0.3)
            progress((i+1), 10)

        return self.url
    run2.description = 'downloading with run2' # property(str, lambda self: 'downloading {}'.format(self.url))

    @uitask(Indefinite)
    def run3(self):
        time.sleep(1)
        return self.url
    run3.description = 'running with run3' # property(str, lambda self: 'downloading {}'.format(self.url))


def run_background_task_samples():
    # long_operation()
    long_operation_with_progress()
    # long_operation_with_arguments('bar')

    # downloader = Downloader('http://kernel.org')
    # downloader.run()
    # downloader.run2('foo')
    # downloader.run3()
