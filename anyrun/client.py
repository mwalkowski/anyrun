import json
import logging
import random
import string

import websocket
from typing import Callable


LOGGER = logging.getLogger(__name__)


class AnyRunClient:

    def __init__(self, on_message_cb: Callable[[dict], None], enable_trace=False):
        self._on_message_cb = on_message_cb
        websocket.enableTrace(enable_trace)
        self._con = None
        self._con_params = {
            'id': 0,
            'token': ''
        }

    def connect(self):
        self._con_params = {
            'id': random.randint(100, 999),
            'token': AnyRunClient._generate_token()
        }

        url = "wss://app.any.run/sockjs/{id}/{token}/websocket".format(
                id=self._con_params['id'],
                token=self._con_params['token']
            )
        LOGGER.debug('Trying to connect to %s', url)
        self._con = websocket.WebSocketApp(
            url=url,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close
        )
        self._con.on_open = self._init_connection

    def run_forever(self):
        self._con.run_forever()

    def _init_connection(self):
        self.send_message({"msg": "connect", "version": "1", "support": ["1", "pre2", "pre1"]})
        self.send_message({"msg": "method", "method": "host", "params": [], "id": "1"})
        self.send_message({"msg": "method", "method": "getPrefix", "params": [], "id": "2"})
        self.send_message({"msg": "sub", "id": "7R8mscvqqAEpbCyBx", "name": "meteor.loginServiceConfiguration", "params": []})
        self.send_message({"msg": "sub", "id": "HyEwZt4iEBwAJQ5Po", "name": "activeTasks", "params": []})
        self.send_message({"msg": "sub", "id": "MzosbATCBsTorHkSP", "name": "settings", "params": []})
        self.send_message({"msg": "sub", "id": "7YLQDHpGxo7hMqEPi", "name": "teams", "params": []})
        self.send_message({"msg": "sub", "id": "6wsnfPru4MT96FzYQ", "name": "tasksHistoryCounter", "params": []})
        self.send_message({"msg": "sub", "id": "Fa3XJ8E6CizGJStD5", "name": "publicTasks",
                           "params": [50, 0, {
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
                            }]
                            })
        self.send_message({"msg": "sub", "id": "Qm8atEvRigconSZHw", "name": "publicTasksCounter",
                           "params": [{
                                "isPublic": True,
                                "hash": "",
                                "major": "",
                                "bit": "",
                                "runtype": [],
                                "name": "",
                                "verdict":[],
                                "specs": [],
                                "ext": [],
                                "tag": "",
                                "significant": False,
                                "ip": "",
                                "fileHash": "",
                                "mitreId": "",
                                "sid": 0,
                                "skip": 0
                            }]
                            })

    def send_message(self, msg: dict) -> None:
        self._con.send(json.dumps([json.dumps(msg)]))

    @staticmethod
    def _generate_token() -> str:
        letters = string.ascii_lowercase + '1234567890'
        return ''.join(random.choice(letters) for _ in range(8))

    def _on_message(self, message) -> None:
        if len(message) > 1:
            message = json.loads(message[1:])[0]
            message = json.loads(message)
            if 'msg' in message and message['msg'] == 'ping':
                LOGGER.debug('Send ping message')
                self.send_message({"msg": "pong"})
            elif self._on_message_cb:
                self._on_message_cb(message)

    def _on_error(self, error) -> None:
        LOGGER.error('ERROR %s', error)

    def _on_close(self) -> None:
        LOGGER.info("Connection closed")
