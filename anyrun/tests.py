import json
from unittest import TestCase, mock
from unittest.mock import Mock, call

from anyrun.client import AnyRunClient, AnyRunException


@mock.patch('anyrun.client.websocket')
class AnyRunClientTest(TestCase):

    def setUp(self) -> None:
        self.cb_mock = Mock()
        self.uut = AnyRunClient(self.cb_mock)
        AnyRunClient.generate_token = AnyRunClientTest.generate_token_stub
        AnyRunClient.generate_id = AnyRunClientTest.generate_id_stub

    def test_connect_call(self, ws_mock):
        self.uut.connect()
        ws_mock.WebSocketApp.assert_called_once_with(
            url="wss://app.any.run/sockjs/{id}/{token}/websocket".format(
                id=AnyRunClientTest.generate_id_stub(),
                token=AnyRunClientTest.generate_token_stub()
            ),
            on_message=self.uut.on_message,
            on_error=self.uut.on_error,
            on_close=self.uut.on_close
        )

    def test_initial_messages(self, ws_mock):
        self.uut.connect()
        ws_mock.WebSocketApp().on_open()

        ws_mock.WebSocketApp().send.assert_has_calls([
            call(AnyRunClientTest.build_message({"msg": "connect", "version": "1", "support": ["1", "pre2", "pre1"]})),
            call(AnyRunClientTest.build_message({"msg": "method", "method": "host", "params": [], "id": "1"})),
            call(AnyRunClientTest.build_message({"msg": "method", "method": "getPrefix", "params": [], "id": "2"})),
            call(AnyRunClientTest.build_message({
                'msg': 'sub',
                'id': AnyRunClientTest.generate_token_stub(),
                'name': 'meteor.loginServiceConfiguration',
                'params': []})),
            call(AnyRunClientTest.build_message({
                'msg': 'sub',
                'id': AnyRunClientTest.generate_token_stub(),
                'name': 'activeTasks',
                'params': []}
            )),
            call(AnyRunClientTest.build_message({
                'msg': 'sub',
                'id': AnyRunClientTest.generate_token_stub(),
                'name': 'settings',
                'params': []}
            )),
            call(AnyRunClientTest.build_message({
                'msg': 'sub',
                'id': AnyRunClientTest.generate_token_stub(),
                'name': 'teams',
                'params': []}
            )),
            call(AnyRunClientTest.build_message({
                'msg': 'sub',
                'id': AnyRunClientTest.generate_token_stub(),
                'name': 'tasksHistoryCounter',
                'params': []}
            )),
            call(AnyRunClientTest.build_message({
                'msg': 'sub',
                'id': AnyRunClientTest.generate_token_stub(),
                'name': 'publicTasks',
                'params': [
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
                    }]}
            )),
            call(AnyRunClientTest.build_message({
                'msg': 'sub',
                'id': AnyRunClientTest.generate_token_stub(),
                'name': 'publicTasksCounter',
                'params': [{
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
                }]}
            )),
        ])

    def test_on_message_server_sends_empty_msg(self, ws_mock):
        self.uut.connect()
        self.uut.on_message('a')

        self.cb_mock.assert_not_called()
        ws_mock.WebSocketApp().send.assert_not_called()

    def test_on_message_server_sends_ping(self, ws_mock):
        self.uut.connect()
        self.uut.on_message('a' + AnyRunClientTest.build_message({'msg': 'ping'}))

        ws_mock.WebSocketApp().send.assert_called_once_with(AnyRunClientTest.build_message({'msg': 'pong'}))

    def test_on_message_server_sends_msg(self, _):
        self.uut.connect()
        self.uut.on_message('a' + AnyRunClientTest.build_message({'msg': 'test'}))

        self.cb_mock.assert_called_once_with({'msg': 'test'})

    def test_on_message_without_cb(self, ws_mock):
        self.uut = AnyRunClient(None)
        self.uut.connect()
        self.uut.on_message('a' + AnyRunClientTest.build_message({'msg': 'test'}))

        self.cb_mock.assert_not_called()
        ws_mock.WebSocketApp().send.assert_not_called()

    def test_call_run_forever(self, ws_mock):
        self.uut.connect()
        self.uut.run_forever()

        self.assertEqual(ws_mock.WebSocketApp().run_forever.call_count, 1)

    def test_call_on_error_raises_exception(self, _):
        with self.assertRaises(AnyRunException):
            self.uut.on_error('error')

    def test_call_on_error_not_raises_exception(self, _):
        self.uut.on_error(KeyboardInterrupt)

    @staticmethod
    def build_message(msg) -> str:
        return json.dumps([json.dumps(msg)])

    @staticmethod
    def generate_token_stub() -> str:
        return 'test'

    @staticmethod
    def generate_id_stub() -> int:
        return 1
