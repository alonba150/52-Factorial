from Core.Server import Server, ServerCommand
from Game.GameManager import *
from Storage.database import *

import threading
from TestClient._TestClient import _TestClient


def get_game():
    with open("game_one.txt", "r") as file:
        game = file.read().replace('\n', '').split("____")
        return game


class GameServer(Server):

    def __init__(self):
        super().__init__(encrypted=False, input_handler=self.__input_handle, name='Game Server', port=55555,
                         display_errors=True)

        # Setting up variables

        t = threading.Thread(target=self.get_input)
        t.start()

        self.__games: List[Game] = []
        self.__client_users = {}

        # Adding all commands

        self.add_command(ServerCommand('connect', self.connect_to_game))
        self.add_command(ServerCommand('play', self.play_game))

        """
        ping_command = ServerCommand('ping', self.ping)
        self.add_command(ping_command)

        admin_command = ServerCommand('admin', self.admin)
        self.add_command(admin_command)

        login_command = ServerCommand('login', self.login)
        self.add_command(login_command)

        logout_command = ServerCommand('logout', self.logout)
        self.add_command(logout_command)

        user_command = ServerCommand('user')
        user_command.add_sub_command('create', self.create_user)
        self.add_command(user_command)

        offer_command = ServerCommand('offer')
        offer_command.add_sub_command('all', self.get_all_offers)
        offer_command.add_sub_command('get', self.get_offer)
        offer_command.add_sub_command('myoffers', self.get_own_offers)
        offer_command.add_sub_command('create', self.create_offer)
        self.add_command(offer_command)

        purchase_command = ServerCommand('purchase')
        purchase_command.add_sub_command('create', self.create_purchase)
        purchase_command.add_sub_command('mypurchases', self.get_own_purchases)
        purchase_command.add_sub_command('dispute', self.delete_purchase)
        purchase_command.add_sub_command('review', self.review_purchase)
        self.add_command(purchase_command)
        
        """
        game = get_game()
        print(game)
        self.game = Game(*game)
        self.game.send_update = self.send_update

        # Configuring Events

        # self.connect_client_event += lambda client: if self.game: self.game.connect(client)
        # self.terminate_client_event += lambda client, *args, **kwargs: self.disconnect_from_game(b"", client)
        # self.terminate_client_event += lambda client, *args, **kwargs: self.log_out(b"", client, kicked=True)

        # Starting self

        self.start()

    def send_update(self, bundles):
        print("HERE0")
        for client in self.clients:
            print("HERE1")
            if self._client_info[client]['addr'] in self.game.players:
                print("HERE2")
                self.send(client, bundles[self.game.players.index(self._client_info[client]['addr'])].encode())

    def issue_handle(fail_message=False):
        """
        Decorator that handles errors and issues within the command functions
        :fail_message: by default returns False if anything didn't go accordingly
        """

        def decorator(func):
            def applicator(self, command: bytes, client, *args, **kwargs):
                try:
                    if not func(self, command, client, *args, **kwargs):
                        self._client_messages[client].append(str(fail_message).encode())
                except Exception as exe:
                    self._client_messages[client].append(str(fail_message).encode())
                    print(exe)
                # print(fail_message)

            return applicator

        return decorator

    def get_input(self):
        while 1:
            try:
                self.broadcast(input("").encode())
            except (KeyboardInterrupt, UnicodeDecodeError):
                self.shut_down("Because of a Manual Stop")
                quit()

    def __input_handle(self, client, addr, data):
        self._client_msg(data, addr)

    @issue_handle()
    def log_in(self, arg: bytes, client, *args, **kwargs):
        if user_id := UserDB.get_id(email=arg[0], password=arg[1]):
            self.__client_users[client] = user_id
            self._client_messages[client].append(str(user_id).encode())
        else:
            self._client_messages[client].append("False".encode())
        return True

    @issue_handle()
    def log_out(self, arg: bytes, client, kicked=False, *args, **kwargs):
        v = self.__client_users.pop(client, False)
        if not kicked:
            if v:
                self._client_messages[client].append("True".encode())
            else:
                self._client_messages[client].append("False".encode())
        return True

    @issue_handle(fail_message="Bad Arguments")
    def sign_in(self, arg: bytes, client, *args, **kwargs):
        self.__client_users[client] = user_id = UserDB.create(username=arg[0], email=arg[1], password=arg[2])
        self._client_messages[client].append(str(user_id).encode())
        return True

    def connect_to_game(self, arg: bytes, client, addr, *args, **kwargs):
        if self.game: self.game.connect(addr)
        return True

    def disconnect_from_game(self, arg: bytes, client, addr, *args, **kwargs):
        if self.game: self.game.disconnect(addr)
        return True

    def play_game(self, arg: bytes, client, addr, *args, **kwargs):
        self.game.activate(addr, [])
        return True

    @issue_handle(fail_message="Bad Arguments")
    def add_game(self, arg: bytes, client, *args, **kwargs):
        if user_id := self.__client_users.get(client, None):
            game_id = GameDB.create(user_id=user_id, code=arg)
            self._client_messages[client].append(str(game_id).encode())
        else:
            self._client_messages[client].append("Not Logged In".encode())
        return True


def do_client():
    _TestClient()


if __name__ == '__main__':
    GameServer()
    # for i in range(4):
    #     t = threading.Thread(target=do_client)
    #     t.start()
