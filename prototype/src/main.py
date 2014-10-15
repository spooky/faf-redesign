import sys
from ui import Application
from tasks import submitIndefinite, submitProgressive

def callback(result):
    print('callback result: {}'.format(result))

@submitIndefinite('running indefinite', finished=callback)
def long_operation():
    import time
    time.sleep(3)
    return 'a'

@submitProgressive('running with progress', finished=callback)
def long_operation_with_progress(progress):
    import time
    count = 0
    while count < 10:
        time.sleep(0.3)
        print(count)
        progress.emit((count+1)/10)
        count += 1
    return 'b'

if __name__ == '__main__':
    app = Application(sys.argv)
    app.start()

    # long_operation()
    long_operation_with_progress()

    sys.exit(app.exec_())
