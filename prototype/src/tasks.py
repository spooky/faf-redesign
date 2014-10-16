from PyQt5.QtCore import QObject, pyqtSignal
from ui import Application

# TODO: progress(0.3) albo progress(3, 10) -> progress(current, max=1.0):
# TODO: progress in function globals -> wrap.func_globals['progress'] = progress
class Indefinite(QObject):
    '''
        Run task without blocking the UI
    '''
    started = pyqtSignal()
    finished = pyqtSignal(object)
    progress = pyqtSignal(float)
    indefinite = True

    def _operation(self):
        return self.operation(*self.args, **self.kwargs)

    def __init__(self, operation, description, args, kwargs):
        super().__init__()
        self.operation = operation
        self.args = args
        self.kwargs = kwargs
        self.description = description

    def __call__(self):
        self.started.emit()
        try:
            result = self._operation()
        except Exception as ex:
            result = ex
        self.finished.emit(result)


class Progressive(Indefinite):
    indefinite = False

    def _operation(self):
        self.kwargs["progress"] = lambda x: self.progress.emit(x)
        return self.operation(*self.args, **self.kwargs)


def task(klass, started=None, finished=None, progress=None):
    """
        Decorate a function to run in background
    """
    def decorate(operation):
        def wrapper(*args, **kwargs):
            print(getattr(operation, "description", None))
            description = getattr(wrapper, "description", str(operation))
            task = klass(operation, description, args, kwargs)

            if started:
                task.started.connect(started)

            if finished:
                task.finished.connect(finished)

            if progress:
                task.progress.connect(progress)

            return Application.instance().getTaskExecutor().submit(task)

        return wrapper

    return decorate


def uitask(klass, started=None, finished=None, progress=None):
    """
        Decorate a function to run in background and report status to
        the main window
    """
    def on_started(*args, **kwargs):
        status = Application.instance().taskStatus
        status.on_started(*args, **kwargs)
        if started:
            started(*args, **kwargs)

    def on_finished(*args, **kwargs):
        status = Application.instance().taskStatus
        status.on_finished(*args, **kwargs)
        if finished:
            finished(*args, **kwargs)

    def on_progress(*args, **kwargs):
        status = Application.instance().taskStatus
        status.on_progress(*args, **kwargs)
        if progress:
            progress(*args, **kwargs)

    return task(klass,
                started=on_started,
                finished=on_finished,
                progress=on_progress)
