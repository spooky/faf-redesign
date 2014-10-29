import logging
from PyQt5.QtCore import QObject
from PyQt5.QtNetwork import QTcpSocket, QHostAddress

# HOST = 'lobby.faforever.com'
# PORT = 8001
HOST = 'localhost'
PORT = 1234


class Client(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.log = logging.getLogger(__name__)
        self._socket_setup()

    def _socket_setup(self):
        self.socket = QTcpSocket(self)
        self.socket.setSocketOption(QTcpSocket.KeepAliveOption, 1)

        self.socket.connected.connect(self.on_connected)
        self.socket.disconnected.connect(self.on_disconnected)
        self.socket.readyRead.connect(self.on_readyRead)
        self.socket.error.connect(self.on_error)
        self.socket.stateChanged.connect(self.on_stateChanged)

    def connect(self, host=HOST, port=PORT):
        if not self.socket.isOpen():
            self.log.info('connecting to {}:{}'.format(host, port))
            self.socket.connectToHost(QHostAddress(host), port)

    def disconnect(self):
        self.log.info('disconnecting')
        self.socket.disconnectFromHost()

    def on_readyRead(self):
        data = bytes()
        while self.socket.bytesAvailable():
            data += self.socket.read(1024)

        self.log.debug(data)

    def on_connected(self):
        self.log.info('connected')

    def on_disconnected(self):
        self.log.info('disconnected')

    def on_error(self, error):
        self.log.error('error {}: {}'.format(error, self.socket.errorString()))

    def on_stateChanged(self, state):
        states = ['Unconnected', 'HostLookup', 'Connecting', 'Connected', 'Bound', 'Closing', 'Listening']
        self.log.debug('state changed to {}'.format(states[state]))
