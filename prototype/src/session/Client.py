import logging
import asyncio
from PyQt5.QtCore import QObject
from PyQt5.QtNetwork import QTcpSocket
from .FafProtocolAdapter import FafProtocolAdapter

UUID = ''
try:
    import private
    UUID = private.UUID
except ImportError:
    pass

HOST = 'lobby.faforever.com'
PORT = 8001
# HOST = 'localhost'
# PORT = 1234


class Client(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.log = logging.getLogger(__name__)
        self._socket = None
        self._awaiting_for_response = dict()

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
        response = self._protocol.receive()
        if response:
            self.log.debug('received {}'.format(response))

        command = response['command'] if response and 'command' in response else None
        if command in self._awaiting_for_response:
            self._awaiting_for_response[command].set_result(response)

    def _on_disconnected(self):
        self.log.info('disconnected')
        self._socket = None

    def _on_stateChanged(self, state):
        states = ['Unconnected', 'HostLookup', 'Connecting', 'Connected', 'Bound', 'Closing', 'Listening']
        self.log.debug('state changed to {} ({})'.format(states[state], state))

    @asyncio.coroutine
    def _get_session(self, user):
        self.log.debug('sending ask_session')
        self._protocol.send(dict(command='ask_session'), user)

        f = asyncio.Future()
        self._awaiting_for_response['welcome'] = f
        return f

    @asyncio.coroutine
    def _hello(self, session, user, hash):
        local_ip = self._socket.localAddress().toString()
        unique_id = UUID
        self.log.debug('sending hello')
        self._protocol.send(dict(command='hello', session=session, login=user, password=hash, version=0, unique_id=unique_id, local_ip=local_ip), user, session)

        f = asyncio.Future()
        self._awaiting_for_response['welcome'] = f
        return f

    @asyncio.coroutine
    def login(self, user, password):
        import hashlib
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        yield from self._connect()
        resp = yield from self._get_session(user)
        start_state = yield from self._hello(resp['session'], user, password_hash)
        self.log.debug('response to hello')
        self.log.debug(start_state)

        return start_state
