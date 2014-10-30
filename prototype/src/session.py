import logging
import json
from PyQt5.QtCore import QObject, QDataStream, QIODevice, QByteArray
from PyQt5.QtNetwork import QTcpSocket

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
        self._socket_setup()

        self._connected = False

    def _socket_setup(self):
        self.socket = QTcpSocket(self)
        self.socket.setSocketOption(QTcpSocket.KeepAliveOption, 1)

        self.socket.connected.connect(self._on_connected)
        self.socket.disconnected.connect(self._on_disconnected)
        self.socket.readyRead.connect(self._on_readyRead)
        self.socket.error.connect(self._on_error)
        self.socket.stateChanged.connect(self._on_stateChanged)

    def _connect(self, host=HOST, port=PORT):
        if not self._connected:
            self.log.info('connecting to {}:{}'.format(host, port))
            self.socket.connectToHost(host, port)
            self._connected = True

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
