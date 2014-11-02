import logging
from PyQt5.QtCore import QObject
from PyQt5.QtNetwork import QTcpSocket
from .FafProtocolAdapter import FafProtocolAdapter

HOST = 'lobby.faforever.com'
PORT = 8001
# HOST = 'localhost'
# PORT = 1234


class Client(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.log = logging.getLogger(__name__)
        self._socket_setup()

        self._connecting = False

    def _socket_setup(self):
        self.socket = QTcpSocket(self)
        self.socket.setSocketOption(QTcpSocket.KeepAliveOption, 1)

        self.socket.connected.connect(self._on_connected)
        self.socket.disconnected.connect(self._on_disconnected)
        self.socket.readyRead.connect(self._on_readyRead)
        self.socket.error.connect(self._on_error)
        self.socket.stateChanged.connect(self._on_stateChanged)

    def _connect(self, host=HOST, port=PORT):
        if not self._connecting:
            self.log.info('connecting to {}:{}'.format(host, port))
            self.socket.connectToHost(host, port)
            self._connecting = True

    def _disconnect(self):
        self.log.info('disconnecting')
        self.socket.disconnectFromHost()

    def _on_readyRead(self):
        self.log.debug('received {}'.format(self._protocol.receive()))

    def _on_connected(self):
        self.log.info('connected')
        self._protocol = FafProtocolAdapter(self.socket)
        self._protocol.send(dict(command='ask_session'), self.user)

    def _on_disconnected(self):
        self.log.info('disconnected')

    def _on_error(self, error):
        self.log.error('error {}: {}'.format(error, self.socket.errorString()))

    def _on_stateChanged(self, state):
        states = ['Unconnected', 'HostLookup', 'Connecting', 'Connected', 'Bound', 'Closing', 'Listening']
        self.log.debug('state changed to {} ({})'.format(states[state], state))

    def login(self, user, password, callback, errback):
        self._connect()
        self.user = user
        # import hashlib
        # self.password_hash = hashlib.md5(str(password))

    def startup_state(self):
        ''' sends the hello command to get current games state '''
        pass

    def available_games(self):
        pass
