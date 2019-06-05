import json
import logging
import random
import string

import websocket
from typing import Callable

LOGGER = logging.getLogger(__name__)


class AnyRunException(Exception):
    pass


class AnyRunClient:

    def __init__(self, on_message_cb: Callable[[dict], None], enable_trace=False):
        self._on_message_cb = on_message_cb
        websocket.enableTrace(enable_trace)
        self._con = None

    def connect(self):
        url = "wss://app.any.run/sockjs/{id}/{token}/websocket".format(
            id=AnyRunClient.generate_id(),
            token=AnyRunClient.generate_token()
        )

        LOGGER.debug('Trying to connect to %s', url)
        self._con = websocket.WebSocketApp(
            url=url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        self._con.on_open = self._init_connection

    def run_forever(self):
        self._con.run_forever()

    def send_message(self, msg: dict) -> None:
        self._con.send(json.dumps([json.dumps(msg)]))

    def _init_connection(self):
        self.send_message({"msg": "connect", "version": "1", "support": ["1", "pre2", "pre1"]})
        self.send_message({"msg": "method", "method": "host", "params": [], "id": "1"})
        self.send_message({"msg": "method", "method": "getPrefix", "params": [], "id": "2"})
        self.subscribe('meteor.loginServiceConfiguration')
        self.subscribe('activeTasks')
        self.subscribe('settings')
        self.subscribe('teams')
        self.subscribe('tasksHistoryCounter')
        self.subscribe('publicTasks', [
            50, 0, {
                "isPublic": True,
                "hash": "",
                "major": "",
                "bit": "",
                "runtype": [],
                "name": "",
                "verdict": [],
                "specs": [],
                "ext": [],
                "tag": "",
                "significant": False,
                "ip": "",
                "fileHash": "",
                "mitreId": "",
                "sid": 0,
                "skip": 0
            }])
        self.subscribe('publicTasksCounter', [{
            "isPublic": True,
            "hash": "",
            "major": "",
            "bit": "",
            "runtype": [],
            "name": "",
            "verdict": [],
            "specs": [],
            "ext": [],
            "tag": "",
            "significant": False,
            "ip": "",
            "fileHash": "",
            "mitreId": "",
            "sid": 0,
            "skip": 0
        }])

    def subscribe(self, name: str, params: list = None) -> None:
        if not params:
            params = []

        self.send_message({'msg': 'sub', 'id': AnyRunClient.generate_token(), 'name': name, 'params': params})

    @staticmethod
    def generate_token() -> str:
        letters = string.ascii_lowercase + '1234567890'
        return ''.join(random.choice(letters) for _ in range(8))

    @staticmethod
    def generate_id() -> int:
        return random.randint(100, 999)

    def on_message(self, message) -> None:
        if len(message) > 1:
            message = json.loads(message[1:])[0]
            message = json.loads(message)
            if 'msg' in message and message['msg'] == 'ping':
                LOGGER.debug('Send ping message')
                self.send_message({"msg": "pong"})
            elif self._on_message_cb:
                self._on_message_cb(message)

    def on_error(self, error) -> None:
        if not isinstance(KeyboardInterrupt, type(error)):
            LOGGER.error('Connection error occurs (%s)', str(error))
            raise AnyRunException(error)

    def on_close(self) -> None:
        LOGGER.info("Connection closed")
