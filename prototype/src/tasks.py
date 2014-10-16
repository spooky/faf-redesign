from PyQt5.QtCore import QObject, pyqtSignal
from ui import Application

# TODO: queue tasks

class IndefiniteTask(QObject):
    '''
        Run task that does not report progress without blocking the UI
    '''
    finished = pyqtSignal(object)

    def _execute_operation(self):
        return self.operation()

    def __init__(self, operation, parent=None):
        super().__init__(parent)
        self.operation = operation

    def __call__(self):
        result = self._execute_operation()
        self.finished.emit(result)

class ProgressiveTask(IndefiniteTask):
    '''
        Run task that can report progress without blocking the UI
    '''
    progress = pyqtSignal(float)

    def _execute_operation(self):
        return self.operation(self.progress)

def submitIndefinite(text, finished=None):
    '''
        Decorator for functions that should be run as an IndefiniteTask
    '''
    def wire(worker):
        task = IndefiniteTask(worker)
        if finished:
            task.finished.connect(finished)

        def submit():
            app = Application.instance()
            app.mainWindow.model.setTaskStatus(text + '...') # throbber?
            task.finished.connect(app.mainWindow.model.clearTaskStatus)

            app.getTaskExecutor().submit(task)

        return submit
    return wire

def submitProgressive(text, finished=None):
    '''
        Decorator for functions that should be run as a ProgressiveTask
    '''
    def wire(worker):
        task = ProgressiveTask(worker)
        if finished:
            task.finished.connect(finished)

        def submit():
            app = Application.instance()
            app.mainWindow.model.setTaskStatus(text, indefinite=False)
            task.finished.connect(app.mainWindow.model.clearTaskStatus)
            def progress(value):
                app.mainWindow.model.taskStatusProgress = value
            task.progress.connect(progress)

            app.getTaskExecutor().submit(task)

        return submit
    return wire
