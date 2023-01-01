import socket
from socket import *
import ssl
import time
import pickle
import Utils.SocketUtils as sUtils
import threading
from Utils.Event import Event

from enum import Enum


#
class TerminationState(Enum):
    FAILED_START = 0
    CLOSED_CONNECTION = 1
    SERVER_SHUTDOWN = 2
    CLIENT_ERROR = 3


class Client:

    def __init__(self, server_addr=None, encrypted: bool = True, sum_length: int = 8,
                 port_server_addr=(gethostbyname(gethostname()), 55555), server_name: str = None):
        # Helper settings
        sUtils.set_length_buff(sum_length)
        self.port_server_addr = port_server_addr

        # Server side variables
        self.is_connected = False
        self.server_info = {}

        # Server connection variables
        self.encrypted = encrypted
        self.server_addr = server_addr
        self.is_declared_server_addr = bool(server_addr)
        self.server_name = server_name

        self.listen_event = Event()
        self.connection_interrupted_event = Event()

    def connect(self):
        """
        Connects the client to the server and if successful starts listening to the server
        """
        if not self.server_addr: self.__server_addr_listen()
        self.__server_setup()

        self.__is_listening = True
        self.__listen_thread = threading.Thread(target=self.__listen, args=[])
        self.__listen_thread.start()

    def __server_setup(self):
        """
        Tries to connect the client to the server multiple times and in case of failure
        disconnects from the server
        """

        self.is_connected = False
        self.try_to_connect = True
        self.server_info = {}

        self.server_socket = socket(AF_INET, SOCK_STREAM)
        if self.encrypted: self.server_socket = ssl.wrap_socket(self.server_socket, server_side=False)
        _count = 0
        while self.try_to_connect:
            try:
                # Try connecting
                self.server_socket.connect(self.server_addr)
                break
            except (ConnectionError, ssl.SSLError):
                # If error occurres more than 20 times, raise error
                if _count > 4:
                    if self.is_declared_server_addr:
                        print('Server not online')
                        self.__connection_interrupted(TerminationState.FAILED_START)
                    else:
                        self.__server_addr_listen()
                    _count = -1
                _count += 1
                time.sleep(1)
            except OSError:
                if self.is_declared_server_addr: print('Server not online')
                self.__connection_interrupted(TerminationState.FAILED_START)
            except:
                raise

        if self.try_to_connect:
            self.is_connected = True

    def __server_addr_listen(self):
        """
        If the server is reachable via a port-server, tries to find it's ip
        """
        while True:
            broadcast_socket = socket(AF_INET, SOCK_STREAM)
            response = ''
            try:
                broadcast_socket.connect(self.port_server_addr)
                broadcast_socket.send('get'.encode())
                response = broadcast_socket.recv(1024)
            except KeyboardInterrupt:
                quit()
            except:
                pass
            broadcast_socket.close()
            if not response:
                print("Port Server Not Online")
                quit()
            else:
                servers = ''
                try:
                    servers = dict(pickle.loads(response))
                except pickle.UnpicklingError:
                    print("The port server does not uphold the specified standards")
                    quit()
                if type(servers) == dict:
                    print("The port server does not uphold the specified standards")
                    quit()
                if len(list(servers.keys())) < 1:
                    time.sleep(1)
                    continue
                if self.server_name:
                    for s_addr in servers.keys():
                        if servers.get(s_addr) == self.server_name: self.server_addr = s_addr
                else:
                    self.server_addr = list(servers.keys())[0]
                break

    def send(self, data):
        """
        Sends data to the server
        :param data: data to send
        """
        if self.is_connected: sUtils.send_message(self.server_socket, data)

    def __listen(self):
        """
        Listens to the server while it's connected to it and passes message handling to
        the listen event for parent class usage
        """
        while self.is_connected:
            data, succeed = sUtils.listen_for_socket(self.server_socket)

            if not self.is_connected:
                break

            # If server does not respond, disconnect
            if not succeed:
                self.__connection_interrupted(TerminationState.SERVER_SHUTDOWN)
                break

            try:
                self.listen_event(data)
            except:
                # self.__connection_interrupted(TerminationState.CLIENT_ERROR)
                pass

    def __connection_interrupted(self, termination_state):
        """
        Abandons connection with server due to a specified reason
        :param termination_state: reason for the lost connection
        """
        print('Disconnected from server', termination_state)
        self.connection_interrupted_event(termination_state)
        if not termination_state == TerminationState.FAILED_START:
            self.server_socket.close()
        else:
            self.try_to_connect = False
        self.is_connected = False

    def terminate_connection(self):
        """
        Ends the connection with the server via client
        """
        if self.is_connected:
            self.__connection_interrupted(TerminationState.CLOSED_CONNECTION)
        else:
            self.try_to_connect = False

    def add_listen_event(self, event):
        """
        Adds a specified event for processing server messages
        :param event: event that will process server messages
        """
        self.listen_event += event

    def add_listen_once_event(self, event):
        """
        Adds a specified event for processing server messages that will
        only work until specified
        :param event: event that will process server messages and return True or False
        depending of choice (True will stop listening, False will continue)
        """

        def listen_once(data):
            if event(data): self.listen_event -= listen_once

        self.listen_event += listen_once


if __name__ == '__main__':
    Client()
