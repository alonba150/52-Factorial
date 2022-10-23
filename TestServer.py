import socket


def server_program():
    host = socket.gethostbyname_ex(socket.gethostname())[-1][-1]
    port = 55555
    print(socket.gethostbyname_ex(socket.gethostname()), host, port)

    server_socket = socket.socket()
    server_socket.bind((host, port))

    server_socket.listen(2)
    while 1:
        conn, address = server_socket.accept()
        print("Connection from: " + str(address))
        try:
            while True:
                data = input(' -> ')
                if not data:
                    break
                conn.send(data.encode())
        except:
            conn.close()


if __name__ == '__main__':
    server_program()
