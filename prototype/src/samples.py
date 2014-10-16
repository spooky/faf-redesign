import time
from tasks import uitask, Indefinite, Progressive, progress


def callback(result):
    print('callback result: {}'.format(result))


@uitask(Indefinite, finished=callback)
def long_operation():
    time.sleep(3)
    return 'a'
long_operation.description = 'Indefinite'


@uitask(Progressive, finished=callback)
def long_operation_with_progress():
    count = 0
    while count < 10:
        time.sleep(0.3)
        progress((count+1)/10)
        count += 1
    return 'b'
long_operation_with_progress.description = 'Progressive'


@uitask(Progressive, finished=callback)
def long_operation_with_arguments(p1):
    count = 0
    while count < 10:
        time.sleep(0.3)
        progress((count+1)/10)
        count += 1
    return 'b'
long_operation_with_arguments.description = 'Progressive2'


class Downloader:
    def __init__(self, url):
        self.url = url

    @uitask(Progressive)
    def run(self, progress):
        for i in range(0,10):
            time.sleep(0.3)
            progress((i+1)/10)

        return self.url
    run.description = 'Downloading' # property(str, lambda self: 'Downloading {}'.format(self.url))

    @uitask(Progressive)
    def run2(self, p1):
        for i in range(0,10):
            time.sleep(0.3)
            progress((i+1), 10)

        return self.url
    run2.description = 'Downloading2' # property(str, lambda self: 'Downloading {}'.format(self.url))


def run_background_task_samples():
    long_operation()
    long_operation_with_progress()
    long_operation_with_arguments("bar")

    downloader = Downloader("http://kernel.org")
    downloader.run()
    downloader.run2("foo")
