"""
Author: Ran Perry
Handles all tcp communications between 2 sockets
"""
import socket
import ssl

length_buffer = 8


def set_length_buff(buff: int):
    """
    :param buff: new buffer
    :return:
    Change the buffer for the length
    """
    global length_buffer
    length_buffer = buff


def listen_for_socket(sock: socket.socket):
    """
    :param sock: socket to receive with
    :return: returns a tuple of (data/error: str) and (succeed: bool)
    Handles the receive with the socket for a custom buffer and returns it
    """
    length, succeed = listen_for_buff(sock, length_buffer)
    if not succeed:
        return length, succeed
    try:
        length = length.decode()
        if not str(length).isdigit():
            return "ERROR:BadLength", False
    except:
        return "ERROR:BadLength", False
    message, succeed = listen_for_buff(sock, int(length))
    if not succeed:
        return message, succeed
    while len(message) < int(length):
        msg_fragment, succeed = listen_for_buff(sock, int(length) - len(message))
        if not succeed:
            return msg_fragment, succeed
        message += msg_fragment
    return message, succeed


def listen_for_buff(sock: socket.socket, buff: int):
    """
    :param sock: socket to receive with
    :param buff: buffer to receive with
    :return: returns a tuple of (data/error: str) and (succeed: bool)
    Handles the errors regarding receiving from a socket with a buffer
    """
    try:
        recv = sock.recv(buff)
    except socket.timeout:
        return 'ERROR:Timeout', False
    except ConnectionResetError:
        return 'ERROR:ConnectionResetError', False
    except:
        return 'ERROR', False
    if not recv:
        return 'ERROR:None', False
    return recv, True


def send_message(sock, data):
    """
    :param sock: socket to send data with
    :param data: string to send
    :return:
    Sends data with the socket in the correct format
    """

    try:
        if type(data) == str:
            l = len(data.encode())
            sock.send(f"{str(l).zfill(length_buffer)}{data}".encode())
        elif type(data) == bytes:
            l = len(data)
            sock.send(f"{str(l).zfill(length_buffer)}".encode() + data)

    except ssl.SSLError:
        pass

