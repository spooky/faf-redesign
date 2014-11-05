import logging
import json
from PyQt5.QtCore import QDataStream, QIODevice, QByteArray


class FafProtocolAdapter():

    server_actions = ['ACK', 'PING', 'PONG', 'UPDATING_NEEDED', 'LOGIN_AVAILABLE']  # oh joy...
    client_actions = ['VERSION', 'UPLOAD_MOD', 'UPLOAD_MAP', 'CREATE_ACCOUNT', 'FA_CLOSED']

    def __init__(self, socket):
        self._socket = socket
        self._block_size = None
        self.log = logging.getLogger(__name__)

    def _act_on_ack(self, stream):
        b = stream.readQString()
        self.log.debug('ACK for {}b'.format(b))

    def _act_on_ping(self, stream):
        self.log.debug('sending PONG')
        self.send('PONG', self._user)

    def send(self, cmd, user, session=None):
        # needed to react to server actions
        self._user = user
        self._session = session

        stream = QDataStream(self._socket)
        stream.setVersion(QDataStream.Qt_4_2)

        data = cmd if cmd is str else json.dumps(cmd)  # ehh...but what are adapters for...

        block = QByteArray()
        out = QDataStream(block, QIODevice.ReadWrite)
        out.setVersion(QDataStream.Qt_4_2)

        out.writeQString(data)
        out.writeQString(user)
        out.writeQString(str(session or ''))

        stream.writeUInt32(block.size())
        stream.writeRawData(block)

    def receive(self):
        stream = QDataStream(self._socket)
        stream.setVersion(QDataStream.Qt_4_2)

        if self._block_size:
            if self._socket.bytesAvailable() < self._block_size:
                return None  # incomplete frame

            reply = stream.readQString()
            self._block_size = 0
            if reply not in self.server_actions:
                data = json.loads(reply)
                return data
            else:
                self.log.debug('received {}'.format(reply))
                if hasattr(self, '_act_on_' + reply.lower()):
                    getattr(self, '_act_on_' + reply.lower())(stream)
                else:
                    return reply
        else:
            self._block_size = stream.readUInt32()
