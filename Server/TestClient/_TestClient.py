import math
import threading
import time

from TestClient.Core.Client import Client, TerminationState
from socket import *


class _TestClient(Client):
    def __init__(self, server_ip: str = gethostbyname_ex(gethostname())[-1][-1], server_port: int = 56545,
                 encrypted: bool = False, sum_length: int = 8, server_name: str = None, *args, **kwargs):
        super().__init__(encrypted=encrypted, server_addr=(server_ip, 55555))
        print(gethostbyname_ex(gethostname())[-1][-1])

        self.listen_event += self.__listen_for_update

        self.connect()

        t = threading.Thread(target=self.user_input)
        try:
            t.start()
        except:
            pass

        self.send(b'connect')

        self.connection_interrupted_event = self.reconnect

    def reconnect(self, event):
        if event == TerminationState.SERVER_SHUTDOWN:
            pass

    def __listen_for_update(self, data: bytes):
        print(data)

    def user_input(self):
        try:
            while self.is_connected:
                self.send(input('').encode())
        except (KeyboardInterrupt, UnicodeDecodeError):
            pass


if __name__ == '__main__':
    _TestClient()
