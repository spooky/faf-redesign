import sys
from ui import Application
from tasks import task, uitask, Indefinite, Progressive

def callback(result):
    print('callback result: {}'.format(result))

@task(Indefinite, finished=callback)
def long_operation():
    import time
    time.sleep(3)
    return 'a'
long_operation.description = "This is an indefinite operation"

@uitask(Progressive, finished=callback)
def long_operation_with_progress(progress):
    import time
    count = 0
    while count < 10:
        time.sleep(0.3)
        print(count)
        progress((count+1)/10)
        count += 1
    return 'b'
long_operation.description = "This is a progressive operation"

class Downloader:
    def __init__(self, url):
        self.url = url

    @uitask(Progressive)
    def run(self, progress):
        print "Starting download of {}".format(self.url)

        import time
        for i in range(0,10):
            time.sleep(0.3)
            progress((i+1)/10)

        print "Finished download of {}".format(self.url)

        return self.url

    run.description = property(lambda self: "Downloading {}".format(self.url))

if __name__ == '__main__':
    app = Application(sys.argv)
    app.start()

    long_operation()
    long_operation_with_progress()

    downloader = Downloader("http://kernel.org")
    downloader.run()

    sys.exit(app.exec_())
