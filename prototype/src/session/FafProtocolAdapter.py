import json
import logging
from PyQt5.QtCore import QDataStream, QIODevice, QByteArray


class FafProtocolAdapter():

    server_actions = ['ACK', 'PING', 'PONG', 'UPDATING_NEEDED', 'LOGIN_AVAILABLE']  # oh joy...
    client_actions = ['VERSION', 'UPLOAD_MOD', 'UPLOAD_MAP', 'CREATE_ACCOUNT', 'FA_CLOSED']

    def __init__(self, socket):
        self._socket = socket
        self._block_size = 0
        self.log = logging.getLogger(__name__)

    def send(self, cmd, user, session=None):
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
        stream.setVersion(QDataStream.Qt_4_2)

        while not stream.atEnd():
            if self._block_size:
                if self._socket.bytesAvailable() < self._block_size:
                    return None  # incomplete frame`

                reply = stream.readQString()
                self._block_size = 0
                if reply and reply not in self.server_actions:
                    data = json.loads(reply)
                    return data
                else:
                    self.log.debug('received server action')
                    self.log.debug(reply)
                    return reply  # TODO... act on server actions
            else:
                self._block_size = stream.readUInt32()
