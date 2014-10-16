from concurrent.futures import ThreadPoolExecutor 
from PyQt5.QtCore import QObject, QUrl, pyqtProperty, pyqtSignal
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtGui import QGuiApplication


class TaskStatus(QObject):
    def __init__(self, parent):
        super().__init__(parent)

    def on_started(self):
        self.parent().setTaskStatus(self.sender().description, self.sender().indefinite)

    def on_progress(self, p):
        self.parent().taskStatusProgress = p

    def on_finished(self, result):
        self.parent().clearTaskStatus()

class Application(QGuiApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__taskExecutor = ThreadPoolExecutor(max_workers=1)

    def getTaskExecutor(self):
        return self.__taskExecutor

    def start(self):
        self.mainWindow = MainWindow(self)
        self.taskStatus = TaskStatus(self.mainWindow.model)
        self.mainWindow.show()


# TODO: use MetaClass model to handle notifyable properties
class MainWindowViewModel(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._label = 'FA Forever v.dev'

        self._taskRunning = False # wether to show the task indicator
        self._taskStatusText = None # text to show while task is running
        self._taskStatusIsIndefinite = True # wether to hide the progress bar
        self._taskStatusProgress = 0 # progress bar progress value - makes sense only if taskStatusIsIndefinite == True

    @pyqtProperty(str, constant =True)
    def label(self):
        return self._label

    @label.setter
    def label(self, text):
        self._label = text

    taskRunning_changed = pyqtSignal(bool)
    @pyqtProperty(bool, notify=taskRunning_changed)
    def taskRunning(self):
        return self._taskRunning

    @taskRunning.setter
    def taskRunning(self, value):
        self._taskRunning = value
        self.taskRunning_changed.emit(value)

    taskStatusText_changed = pyqtSignal(str)
    @pyqtProperty(str, notify=taskStatusText_changed)
    def taskStatusText(self):
        return self._taskStatusText

    @taskStatusText.setter
    def taskStatusText(self, value):
        self._taskStatusText = value
        self.taskStatusText_changed.emit(value)

    taskStatusIsIndefinite_changed = pyqtSignal(bool)
    @pyqtProperty(bool, notify=taskStatusIsIndefinite_changed)
    def taskStatusIsIndefinite(self):
        return self._taskStatusIsIndefinite

    @taskStatusIsIndefinite.setter
    def taskStatusIsIndefinite(self, value):
        self._taskStatusIsIndefinite = value
        self.taskStatusIsIndefinite_changed.emit(value)

    taskStatusProgress_changed = pyqtSignal(float)
    @pyqtProperty(float, notify=taskStatusProgress_changed)
    def taskStatusProgress(self):
        return self._taskStatusProgress

    @taskStatusProgress.setter
    def taskStatusProgress(self, value):
        self._taskStatusProgress = value
        self.taskStatusProgress_changed.emit(value)

    def setTaskStatus(self, text, indefinite=True):
        self.taskStatusText = text
        self.taskStatusProgress = 0.0
        self.taskStatusIsIndefinite = indefinite
        self.taskRunning = True

    def clearTaskStatus(self):
        self.taskRunning = False
        self.taskStatusIsIndefinite = True
        self.taskStatusText = None
        self.taskStatusProgress = 0.0


class MainWindow(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.model = MainWindowViewModel(self)

        self.engine = QQmlApplicationEngine(self)
        self.engine.rootContext().setContextProperty('model', self.model)
        self.engine.quit.connect(parent.quit)
        self.engine.load(QUrl.fromLocalFile('ui/chrome.qml'))

        self.window = self.engine.rootObjects()[0]

    def show(self):
        self.window.show()
