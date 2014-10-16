from PyQt5.QtCore import QObject, pyqtSignal
from ui import Application

# TODO: queue tasks

class Indefinite(QObject):
    '''
        Run task without blocking the UI
    '''
    started = pyqtSignal(bool)
    finished = pyqtSignal(object)
    progress = pyqtSignal(float)

    def _operation(self):
        return self.operation()

    def __init__(self, operation):
        super().__init__()
        self.operation = operation
        self.description = getattr(operation, "description", str(operation))

    def __call__(self):
        self.started.emit()
        result = self._operation()
        self.finished.emit(result)


class Progressive(Indefinite):
    def _operation(self):
        return self.operation(lambda x: self.progress.emit(x))


def task(klass, started=None, finished=None, progress=None):
    """
        Decorate a function to run in background
    """
    def wire(operation):
        task = klass(operation)

        if started:
            task.started.connect(started)

        if finished:
            task.finished.connect(finished)

        if progress:
            task.progress.connect(progress)

        def submit():
            Application.instance().getTaskExecutor().submit(task)

        return submit
    return wire


def uitask(klass, started=None, finished=None, progress=None):
    """
        Decorate a function to run in background and report status to
        the main window
    """
    status = Application.instance().taskStatus

    def on_started(*args, **kwargs):
        status.on_started(*args, **kwargs)
        if started:
            started()

    def on_finished(*args, **kwargs):
        status.on_finished(*args, **kwargs)
        if finished:
            finished()

    def on_progress(*args, **kwargs):
        status.on_progress(*args, **kwargs)
        if progress:
            progress()

    return task(klass,
                started=on_started,
                finished=on_finished,
                progress=on_progress)

