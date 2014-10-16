import sys
from ui import Application

if __name__ == '__main__':
    app = Application(sys.argv)
    app.start()

    from samples import run_background_task_samples
    run_background_task_samples()

    sys.exit(app.exec_())
