import logging
import json
import asyncio
from PyQt5.QtCore import QObject
from . import AUTH_SERVICE_URL, rest


class Client(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.log = logging.getLogger(__name__)

    @asyncio.coroutine
    def login(self, user, password):
        url = '{}/login'.format(AUTH_SERVICE_URL)

        data = json.dumps({'username': user, 'password': password}).encode()

        body = yield from rest.post(url, data=data)

        self.log.debug(body)

        self.session_id = body['session_id']
        self.user_id = body['user_id']
        self.email = body['email']

        return body['success']

    @asyncio.coroutine
    def logout(self):
        url = '{}/logout'.format(AUTH_SERVICE_URL)

        self.session_id = None
        self.user_id = None
        self.email = None

        return True
