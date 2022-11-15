import socket

"""

Dear programmer:
When I wrote this code, only god and
I knew how it worked.
Now, only god knows.

Therefore, if you are trying to optimize
this and it doesn't work (most likely),
please increase this counter as a warning
for the next individual:

total_hours_wasted_here = 0

"""

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
