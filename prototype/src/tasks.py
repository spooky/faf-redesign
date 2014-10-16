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


def uitask(klass, started=None, finished=None, progress=None):
    '''
        Decorate a function to run in background
    '''
    def decorate(operation):
        import functools

        @functools.wraps(operation)
        def wrapper(*args, **kwargs):
            description = getattr(wrapper, 'description', operation.__name__)
            task = klass(operation, description, args, kwargs)

            def call(f):
                def wrap(*a, **kwa):
                    a = args + a
                    kwa.update(kwargs)
                    f(*a, **kwa)
                return wrap

            status = Application.instance().taskStatus

            task.started.connect(status.on_started)
            if started:
                task.started.connect(call(started))

            task.finished.connect(status.on_finished)
            if finished:
                task.finished.connect(call(finished))

            task.progress.connect(status.on_progress)
            if progress:
                task.progress.connect(call(progress))

            return Application.instance().getTaskExecutor().submit(task)
        return wrapper
    return decorate


def progress(*args, **kwargs):
    '''
        Stub to silence symbol warnings in task-decorated functions
    '''
    pass
