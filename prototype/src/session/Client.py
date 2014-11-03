import logging
from PyQt5.QtCore import QObject
from PyQt5.QtNetwork import QTcpSocket
from .FafProtocolAdapter import FafProtocolAdapter

import asyncio

HOST = 'lobby.faforever.com'
PORT = 8001
# HOST = 'localhost'
# PORT = 1234


class Client(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.log = logging.getLogger(__name__)
        self._socket = None

    @asyncio.coroutine
    def _connect(self, host=HOST, port=PORT):
        f = asyncio.Future()

        if self._socket is not None:
            f.set_exception(Exception("Client is already connecting"))

        self._socket = QTcpSocket(self)
        self._socket.setSocketOption(QTcpSocket.KeepAliveOption, 1)

        def on_connected():
            self.log.info('connected')
            self._protocol = FafProtocolAdapter(self._socket)

            self._socket.disconnected.connect(self._on_disconnected)
            self._socket.readyRead.connect(self._on_readyRead)

            f.set_result(None)

        def on_error(error):
            f.set_exception(error)

        self._socket.connected.connect(on_connected)
        self._socket.error.connect(on_error)
        self._socket.stateChanged.connect(self._on_stateChanged)

        self.log.info('connecting to {}:{}'.format(host, port))
        self._socket.connectToHost(host, port)

        return f

    def _disconnect(self):
        self.log.info('disconnecting')
        self.socket.disconnectFromHost()

    def _on_readyRead(self):
        self.log.debug('received {}'.format(self._protocol.receive()))

    def _on_disconnected(self):
        self.log.info('disconnected')
        self._socket = None

    def _on_stateChanged(self, state):
        states = ['Unconnected', 'HostLookup', 'Connecting', 'Connected', 'Bound', 'Closing', 'Listening']
        self.log.debug('state changed to {} ({})'.format(states[state], state))

    @asyncio.coroutine
    def _get_session(self, user):
        self._protocol.send(dict(command='ask_session'), user)

    @asyncio.coroutine
    def login(self, user, password):
        yield from self._connect()
        yield from self._get_session(user)

        # import hashlib
        # self.password_hash = hashlib.md5(str(password))
