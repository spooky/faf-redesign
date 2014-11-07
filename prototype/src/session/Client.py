import logging
import json
import asyncio
import aiohttp
from PyQt5.QtCore import QObject
from . import AUTH_SERVICE_URL


class ServerError(Exception):
    pass


class Client(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.log = logging.getLogger(__name__)

    @asyncio.coroutine
    def login(self, user, password):
        import hashlib
        pass_hash = hashlib.sha256(password.encode()).hexdigest()
        headers = {'content-type': 'application/json'}
        data = json.dumps({'username': user, 'password': pass_hash}).encode()

        response = yield from aiohttp.request('POST', '{}/login'.format(AUTH_SERVICE_URL), headers=headers, data=data)
        if not response.status < 400:
            error = None
            try:
                error = yield from response.json()
            except:
                error = yield from response.text()

            raise ServerError(error)

        body = yield from response.json()

        self.session_id = body['session_id']
        self.user_id = body['user_id']
        self.email = body['email']

        return body['success']
