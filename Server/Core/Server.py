"""
Author: Ran Perry
"""
# region Imports
import socket

import Utils.SocketUtils as sUtils

import os
import select
from socket import *
import datetime
import ssl
from Utils.Event import Event


# endregion

def get_time():
    """
    :return: Current time without disgusting microseconds
    """
    current_time = datetime.datetime.now()
    current_time = current_time - datetime.timedelta(microseconds=current_time.microsecond)
    return current_time


class ServerCommand:

    def __init__(self, command_syntax: str, command_activation=None, sub_commands=None):
        self.command_syntax = command_syntax.encode()
        self.command_activation = command_activation
        if sub_commands is None:
            sub_commands = []
        self.sub_commands = sub_commands

    def add_sub_command(self, sub_command: str, sub_command_activation):
        """
        :param sub_command: syntax of the sub command
        :param sub_command_activation: call to the function upon activation
        Adds a sub command under this command
        """
        self.sub_commands.append(ServerCommand(sub_command, sub_command_activation))
        return self

    def has_sub_commands(self):
        """
        :return: whether this command has sub commands
        """
        return not self.sub_commands == []

    def execute_with_hierarchy(self, command: bytes, *args, **kwargs):
        """
        A call to the command object that will pass through all sub commands and check to which the command applies
        it then calls the function of the specific sub command or itself
        :param command: command, string
        """

        if command[:len(self.command_syntax) + 1] == self.command_syntax + b' ' and self.has_sub_commands():
            command = command[len(self.command_syntax) + 1:]
            for sub_command in self.sub_commands:
                sub_command.execute_with_hierarchy(command, *args, **kwargs)
            return

        if command[:len(self.command_syntax)] == self.command_syntax:
            command = command[len(self.command_syntax) + 1:]
            if self.command_activation:
                self.command_activation(command, *args, **kwargs)
                return


class Server:

    def __init__(self, encrypted: bool = True, port_server_addr: tuple = None,
                 input_handler=None, name: str = None, default_password: int = 4444,
                 ip: str = gethostbyname_ex(gethostname())[-1][-1], port: int = 54321, display_errors=False):

        # Save start time
        start_time = datetime.datetime.now()
        self.start_time = start_time - datetime.timedelta(microseconds=start_time.microsecond)

        sUtils.set_length_buff(8)

        self.__default_password = default_password
        self.addr = (ip, port)
        self.name = name
        self.encrypted = encrypted
        self.port_server_addr = port_server_addr
        self.display_errors = display_errors
        self.__server_message_history = ""

        self.__is_active = True
        self.__has_started = False

        # Main socket setup
        self.__server = socket(AF_INET, SOCK_STREAM)
        if self.encrypted:
            if not os.path.exists('certificate.pem'): raise FileNotFoundError('certificate file is missing')
            if not os.path.exists('privkey.pem'): raise FileNotFoundError('private key file is missing')
            self.__server = ssl.wrap_socket(self.__server, server_side=True,
                                            certfile='certificate.pem', keyfile='privkey.pem')

        self.__sockets = [self.__server]
        self._client_messages = {}
        self._client_info = {}
        self.__commands = []

        self.__input_handle = None
        if input_handler is not None:
            self.__input_handle = input_handler

        # Events
        self.terminate_client_event = Event()
        self.connect_client_event = Event()

    def start(self):
        """
        Starts the server
        """
        if not self.__has_started:
            self.__has_started = True
            self.__main()

    def broadcast(self, data):
        """
        Broadcasts a message to the entire server
        :param data: message to broadcast
        """
        for client in self.__sockets[1:]:
            self._client_messages[client].append(data)

    def __main(self):
        # Alert server starting process
        self._server_msg(f"Starting Up Server on {self.addr}")

        try:
            self.__server.bind(self.addr)
        except (ConnectionError, ssl.SSLError, OSError):
            self._server_msg("Server Start-Up failed - Server is already running")
            quit()
        self.__server.listen(5)

        # Port server communication and checkup
        if self.port_server_addr: self.add_to_port_server()

        while self.__sockets and self.__is_active:

            try:
                read, write, exception = select.select(self.__sockets, self.__sockets[1:], self.__sockets)
            except KeyboardInterrupt:
                self.shut_down('Manual Stop')
                break  # Unnecessary, only there so pycharm wouldn't yell at me

            # Handle inputs
            for read_client in read:
                if read_client is self.__server:
                    # Accept new connection
                    try:
                        new_client, new_client_addr = read_client.accept()
                    except ssl.SSLError:
                        continue
                    except OSError:
                        self.shut_down('Client Accept Error')
                        break  # Pycharm is yelling at me if I don't do this help me
                    self._server_msg(f"Started connection with {new_client_addr}")
                    new_client.setblocking(False)
                    self.__sockets.append(new_client)
                    self._client_info[new_client] = {}
                    self._client_info[new_client]['addr'] = new_client_addr
                    self._client_info[new_client]['name'] = str(new_client_addr)

                    self._client_messages[new_client] = []
                    self.connect_client_event(new_client)
                else:
                    # Read what client says
                    data, succeed = sUtils.listen_for_socket(read_client)

                    # Error occurred
                    if not succeed:

                        # Client left without notifying :(
                        if data == "ERROR:ConnectionResetError" or data == "ERROR:None":
                            self.terminate_client(read_client, reason='Client has closed the connection')

                        elif data == "ERROR:BadLength":
                            self._server_msg("An error has occurred regarding the socket_message_helper.")
                            self.terminate_client(read_client,
                                                  reason="an error has occurred regarding the socket_message_helper")

                        # Unknown error
                        elif data.startswith("ERROR"):
                            print(data)
                            self._server_msg("An unknown error has occurred.")
                            self.terminate_client(read_client, reason="an unknown error has occurred")
                    else:
                        if self.__input_handle: self.__input_handler(read_client, data)

            # Handle outputs
            for write_client in write:
                if self._client_messages.get(write_client, None):
                    sUtils.send_message(write_client, self._client_messages[write_client].pop(0))

            for exception_client in exception:
                self.terminate_client(exception_client, reason="an unknown error has occurred")
                self._server_msg('Client left due to exception')

    def __time_msg(self, msg):
        """
        Sends message in the server log with time and adds it to the history
        :param msg: msg to send
        :return:
        """

        time_msg = f'{get_time()} | {msg}'
        print(time_msg)
        self.__server_message_history += time_msg + '\n'

    # Decorative lambdas for messages
    def _client_msg(self, msg, addr):
        self.__time_msg(f"[CLIENT {addr}] {msg}")

    def _server_msg(self, msg):
        self.__time_msg(f"[SERVER] {msg}")

    def _broadcast_msg(self, msg, addr):
        self.__time_msg(f"[BROADCAST] [CLIENT {addr}] {msg}")

    # region Commands

    def add_command(self, command: ServerCommand):
        """
        Adds a command to the server
        :param command: command to add
        """
        self.__commands.append(command)

    def add_commands(self, commands: list):
        """
        Adds commands to the server
        :param commands: commands to add
        """
        for command in commands:
            self.add_command(command)

    def remove_command(self, command: ServerCommand):
        """
        Remove a command from the server
        :param command: command to remove
        """
        if command in self.__commands:
            self.__commands.remove(command)
            return True
        return False

    def remove_commands(self, commands: list):
        """
        Remove commands from the server
        :param commands: commands to remove
        """
        return all(self.remove_command(command) for command in commands)

    # endregion

    def __input_handler(self, client, data):
        addr = self._client_info[client]['addr']
        for command in self.__commands:
            try:
                command.execute_with_hierarchy(command=data, client=client, addr=addr)
            except Exception as e:
                if not self.display_errors:
                    self.terminate_client(client, reason=e.__str__())
                else:
                    raise
        try:
            self.__input_handle(client, addr, data)
        except Exception as e:
            if not self.display_errors:
                self.terminate_client(client, reason=e.__str__())
            else:
                raise

    def __connection(self, client, addr, data):
        pass

    def shut_down(self, reason=None):
        """
        Disconnects from all clients
        Saves server log
        Shuts down server
        :return:
        """

        if not self.__is_active:
            return

        if self.port_server_addr: self.delete_from_port_server()

        for client in self.__sockets[1:]:
            self.terminate_client(client, shut_down=True, reason='the server is shutting down')

        self.__sockets.clear()

        self._server_msg(f'Shutting Down Server{f" Because of a {reason}" if reason else ""}')

        with open(os.path.join("../Logs", f'{str(self.start_time).replace(" ", "-").replace(":", "-")}.txt'),
                  'w') as file:
            file.write(self.__server_message_history)
            file.close()

        self.__is_active = False

        self.__server.close()

    def terminate_client(self, client, shut_down=False, reason: str = None):
        """
        Disconnects a client from the server
        :param client: Client to disconnect
        :param shut_down: is the reason for disconnection a server shutdown
        :param reason: reason in string
        """
        self.terminate_client_event(client, shut_down, reason)
        addr = self._client_info[client]['addr']
        self._client_info.pop(client, None)
        self._server_msg(f"Closed connection with {addr}{f' because {reason}' if reason else ''}")
        self.__sockets.remove(client)
        del self._client_messages[client]
        client.close()

    # region Port Server Handling

    def add_to_port_server(self):
        """
        Adds the Server details to the port server
        """
        response = ''
        while not response == "ok":
            if response: print(response)
            broadcast_socket = socket(AF_INET, SOCK_STREAM)
            try:
                broadcast_socket.connect(self.port_server_addr)
                broadcast_socket.send(
                    f'add:{self.name if self.name else input("Enter Server Name: ")}:{self.addr[0]}:{self.addr[1]}'.encode())
                response = broadcast_socket.recv(1024).decode()
            except:
                broadcast_socket.close()
                self._server_msg("Server Start-Up failed - Port Server Not Online")
                quit()
            broadcast_socket.close()
            if not response == 'ok' and self.name:
                self._server_msg("Server Start-Up failed - Port Server encountered an unknown problem")
                quit()

    def delete_from_port_server(self):
        """
        Removes the Server details from the port server
        """
        broadcast_socket = socket(AF_INET, SOCK_STREAM)
        try:
            broadcast_socket.connect(self.port_server_addr)
            broadcast_socket.send(f'del:{self.addr[0]}:{self.addr[1]}'.encode())
        except:
            pass
        broadcast_socket.close()

    # endregion


if __name__ == '__main__':
    Server()
