import logging
# from PyQt5.QtCore import QDataStream
from PyQt5.QtNetwork import QTcpSocket

# LOBBY_HOST = 'lobby.faforever.com'
# LOBBY_PORT = 8001
LOBBY_HOST = '127.0.0.1'
LOBBY_PORT = 1234


class Connection(object):

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        self._socket_setup()

    def _socket_setup(self):
        self.socket = QTcpSocket()
        self.socket.setSocketOption(QTcpSocket.KeepAliveOption, 1)

        self.socket.readyRead.connect(self.on_connected)
        self.socket.disconnected.connect(self.on_disconnected)
        self.socket.error.connect(self.on_error)
        self.socket.stateChanged.connect(self.on_stateChanged)

    def connect(self):
        self.log.info('connecting...')
        self.socket.connectToHost(LOBBY_HOST, LOBBY_PORT)

    def on_connected(self):
        self.log.info('connected')

    def on_disconnected(self):
        self.log.info('disconnected')

    def on_error(self, error):
        self.log.error('error {}: {}'.format(error, self.socket.errorString()))

    def on_stateChanged(self, state):
        states = ['Unconnected', 'HostLookup', 'Connecting', 'Connected', 'Bound', 'Closing', 'Listening']
        self.log.debug('state changed to {}'.format(states[state]))
