import logging
from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal
from utils.async import async_slot
from session.Client import Client


class MainWindowViewModel(QObject):  # TODO: use MetaClass(ish) model to handle notifyable properties?

    def __init__(self, parent=None):
        super().__init__(parent)

        self._label = 'FA Forever v.dev'

        self._taskRunning = False  # wether to show the task indicator
        self._taskStatusText = None  # text to show while task is running
        self._taskStatusIsIndefinite = True  # wether to hide the progress bar
        self._taskStatusProgress = 0  # progress bar progress value - makes sense only if taskStatusIsIndefinite == True

    @pyqtProperty(str, constant=True)
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


class LoginViewModel(QObject):
    login = pyqtSignal(str, str, bool)

    def __init__(self, client, parent=None):
        super().__init__(parent)
        self.log = logging.getLogger(__name__)

        self.login.connect(self.on_login)
        self.client = client

    @async_slot
    def on_login(self, username, password, remember):
        try:
            self.log.info('logging in...')
            result = yield from self.client.login(username, password)
            self.log.debug('login successful? {}'.format(result))
        except Exception as ex:
            self.log.info('login failed: {}'.format(ex))
