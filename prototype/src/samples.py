import time
from tasks import uitask, Indefinite, Progressive

def callback(result):
    print('callback result: {}'.format(result))

@uitask(Indefinite, finished=callback)
def long_operation():
    time.sleep(1)
    return 'a'
long_operation.description = "running operation without progress"

@uitask(Progressive, finished=callback)
def long_operation_with_progress(progress):
    steps = 10
    for i in range(0, steps):
        time.sleep(0.3)
        progress((i+1) / steps)
    return 'b'
long_operation_with_progress.description = "running operation and reporting progress"

@uitask(Progressive, finished=callback)
def long_operation_with_arguments(p1, progress):
    steps = 10
    for i in range(0, steps):
        time.sleep(0.3)
        progress((i+1) / steps)
    return 'c'
long_operation_with_arguments.description = "running operation with an argument and reporting progress"

class Downloader:
    def __init__(self, url):
        self.url = url

    @uitask(Progressive)
    def run(self, progress):
        steps = 10
        for i in range(0, steps):
            time.sleep(0.3)
            progress((i+1) / steps)

        return self.url
    run.description = "Downloading" # property(str, lambda self: "Downloading {}".format(self.url))

    @uitask(Progressive)
    def run2(self, p1, progress):
        steps = 10
        for i in range(0, steps):
            time.sleep(0.3)
            progress((i+1) / steps)

        return self.url
    run2.description = "Downloading2" # property(str, lambda self: "Downloading {}".format(self.url))


def run_background_task_samples():
    long_operation()
    long_operation_with_progress()
    long_operation_with_arguments("bar")

    downloader = Downloader("http://kernel.org")
    downloader.run()
    downloader.run2("foo")