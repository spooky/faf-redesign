from PyQt5.QtCore import QObject


class TaskStatus(QObject):

    def __init__(self, parent):
        super().__init__(parent)

    def on_started(self):
        self.parent().setTaskStatus(
            self.sender().description, self.sender().indefinite)

    def on_progress(self, p):
        self.parent().taskStatusProgress = p

    def on_finished(self, result):
        self.parent().clearTaskStatus()
