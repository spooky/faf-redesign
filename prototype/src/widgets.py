from PyQt5.QtCore import QObject, QUrl, pyqtSignal
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtGui import QGuiApplication, QIcon
from PyQt5.QtQuick import QQuickItem
from view_models import MainWindowViewModel, LoginViewModel
from session.Client import Client

LOG_BUFFER_SIZE = 1000


class Application(QGuiApplication):
    log_changed = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.setWindowIcon(QIcon('ui/icons/faf.ico'))
        except AttributeError:
            pass

        # required for settings persistance
        self.setOrganizationName("Forged Alliance Forever")
        self.setOrganizationDomain("faforever.com")
        self.setApplicationName("lobby")

    def start(self):
        self.mainWindow = MainWindow(self)
        self.mainWindow.show()

    def log(self, msg):
        self.log_changed.emit(msg)


class MainWindow(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.client = Client(self)

        self.model = MainWindowViewModel(self)
        self.loginModel = LoginViewModel(self.client, self)

        self.engine = QQmlApplicationEngine(self)
        self.engine.rootContext().setContextProperty('model', self.model)
        self.engine.rootContext().setContextProperty('loginModel', self.loginModel)
        self.engine.quit.connect(parent.quit)
        self.engine.load(QUrl.fromLocalFile('ui/Chrome.qml'))

        self.window = self.engine.rootObjects()[0]

        # wire up logging console
        self.log = self.window.findChild(QQuickItem, 'log')
        parent.log_changed.connect(self._log)

    def show(self):
        self.window.show()

    def _log(self, msg):
        # replace with collections.deque binding(ish)?
        if self.log.property('lineCount') == LOG_BUFFER_SIZE:
            line_end = self.log.property('text').find('\n') + 1
            self.log.remove(0, line_end)

        self.log.append(msg)
