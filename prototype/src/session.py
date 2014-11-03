import logging
import json
from PyQt5.QtCore import QObject, QDataStream, QIODevice, QByteArray
from PyQt5.QtNetwork import QTcpSocket

import asyncio

HOST = 'lobby.faforever.com'
PORT = 8001
# HOST = 'localhost'
# PORT = 1234


class FafProtocolAdapter():

    server_actions = ['ACK', 'PING', 'PONG', 'UPDATING_NEEDED', 'LOGIN_AVAILABLE']  # oh joy...
    client_actions = ['VERSION', 'UPLOAD_MOD', 'UPLOAD_MAP', 'CREATE_ACCOUNT', 'FA_CLOSED']

    def __init__(self, socket):
        self._socket = socket
        self._block_size = None
        self.log = logging.getLogger(__name__)

    def send(self, cmd, user, session=None):  # rename command?
        stream = QDataStream(self._socket)
        stream.setVersion(QDataStream.Qt_4_2)

        data = json.dumps(cmd)

        block = QByteArray()
        out = QDataStream(block, QIODevice.ReadWrite)
        out.setVersion(QDataStream.Qt_4_2)

        out.writeQString(data)
        out.writeQString(user)
        out.writeQString(session or '')

        stream.writeUInt32(block.size())
        stream.writeRawData(block)

    def receive(self):
        stream = QDataStream(self._socket)

        if self._block_size:
            if self._socket.bytesAvailable() < self._block_size:
                return None  # incomplete frame

            reply = stream.readQString()
            self._block_size = 0
            self.log.debug(reply)
            if reply not in self.server_actions:
                data = json.loads(reply)
                self.log.debug(data)
                return data
            else:
                return reply  # TODO... act on server actions
        else:
            self._block_size = stream.readUInt32()


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
