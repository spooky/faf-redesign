from PyQt5.QtCore import QObject, pyqtSignal
from ui import Application

class Indefinite(QObject):
    '''
        Run task without blocking the UI
    '''
    started = pyqtSignal()
    finished = pyqtSignal(object)
    progress = pyqtSignal(float)
    indefinite = True

    def _progress(self, current, max=1.0):
        self.progress.emit(current / max)

    def __init__(self, operation, description, args, kwargs):
        super().__init__()
        self.operation = operation
        self.description = description
        self.args = args
        self.kwargs = kwargs

        # inject "progress" function into operation's scope
        self.operation.__globals__['progress'] = self._progress

    def __call__(self):
        self.started.emit()
        try:
            result = self.operation(*self.args, **self.kwargs)
        except Exception as ex:
            result = ex
        self.finished.emit(result)


class Progressive(Indefinite):
    indefinite = False


def task(klass, started=None, finished=None, progress=None):
    '''
        Decorate a function to run in background
    '''
    def decorate(operation):
        def wrapper(*args, **kwargs):
            description = getattr(wrapper, 'description', operation.__name__)
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
    '''
        Decorate a function to run in background and report status to
        the main window
    '''
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

def progress(*args, **kwargs):
    '''
        Stub to silence symbol warnings in task-decorated functions
    '''
    pass
