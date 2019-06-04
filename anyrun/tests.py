from unittest import TestCase, mock
from unittest.mock import Mock

from anyrun.client import AnyRunClient


@mock.patch('anyrun.client.websocket')
class TestClass(TestCase):

    def setUp(self) -> None:
        self.cb_mock = Mock()
        self.uut = AnyRunClient(self.cb_mock)

    def test_connect_call(self, ws_mock):
        self.uut.connect()

        self.assertNotEqual(self.uut._con_params['id'], 0)
        self.assertNotEqual(self.uut._con_params['token'], '')

        ws_mock.WebSocketApp.assert_called_once_with(
            url="wss://app.any.run/sockjs/{id}/{token}/websocket".format(
                id=self.uut._con_params['id'],
                token=self.uut._con_params['token']
            ),
            on_message=self.uut._on_message,
            on_error=self.uut._on_error,
            on_close=self.uut._on_close
        )
