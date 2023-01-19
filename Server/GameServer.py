from Core.Server import Server, ServerCommand
from Game.GameManager import *
from Storage.database import *

import threading
from TestClient._TestClient import _TestClient


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

        self.game = Game(
            "0: [A000**{(1/2)}*]///1: [C000*{(0.0)}*{(5)}*{(5)//(129)}]///2: [B005*{(0.0)}*{(4)}*]///3: [A000**{(4)}*]///"
            "4: [B003*{(3.0)//(2.0)}*{(6)}*]///5: [B004*{(1.0)}*{(6)}*{(6)}]///6: [C001*{(5.0)//(4.0)}**]///"
            "7: [E000***{(1)}]///129: [A000***]",
            "0: [E001***{(1)}]///"
            "1: [D001*{(5.0)}**{(2)//(129)}]///"
            "2: [C003*{(7.0)//(9.0)//(15.0)}**{(11)}]///"
            "3: [A002**{(5)}*]///"
            "4: [A003**{(5)}*]///"
            "5: [B007*{(3.0)//(4.0)}*{(1)}*]///"
            "6: [A003**{(7/8)}*]///"
            "7: [B008*{(6.0)}*{(2)}*]///"
            "8: [B000*{(6.0)//(17.0)}*{(9)}*]///"
            "9: [B008*{(8.0)}*{(2)}*]///"
            "10: [B009*{(18.0)//(19.0)}*{(14/30)}*]///"
            "11: [D001*{(12.0)}**{(35/36/14)//(40)}]///"
            "12: [B007*{(13.0)//(20.0)}*{(11)}*]///"
            "13: [A003**{(12)}*]///"
            "14: [C000*{(10.0)}*{(39/26)}*{(39)//(30)}]///"   # TODO FIX FOR TRIGGERS
            "15: [N000**{(2)}*]///"
            "17: [N004**{(8)}*]///"
            "18: [N004**{(10)}*]///"
            "19: [N008**{(10)}*]///"
            "20: [N003**{(12)}*]///"
            "21: [N000**{(22)}*]///"
            "22: [B010*{(39.0)//(21.0)}*{(23)}*{(23)}]///"
            "23: [B011*{(22.0)}*{(38/25)}*{(38)}]///"   # TODO ADD /25 back
            "24: [D001*{(38.0)}**{(25/26)//(129)}]///" 
            "25: [F%max%*{(23.0)}**]///"    # TODO FIX VARIABLES
            "26: [F%index%*{(14.0)}**]///"  # TODO FIX VARIABLES
            "27: [G%index%**{(29)}*]///"    # TODO FIX VARIABLES
            "28: [N004**{(29)}*]///"
            "29: [B000*{(27.0)//(28.0)}*{(31)}*]///"
            "30: [C000*{(10.0)}*{(32)}*{(32)//(40)}]///"      # TODO FIX FOR TRIGGERS
            "31: [B008*{(29.0)}*{(33)}*]///"
            "32: [B008*{(30.0)}*{(33)}*{(33)}]///"
            "33: [C003*{(32.0)//(31.0)//(41.0)}**]///"
            "34: [N014**{(35/36)}*]///"
            "35: [F%max%*{(34.0)}**]///"
            "36: [F%index%*{(34.0)}**]///"
            "37: [G%max%**{(38)}*]///"
            "38: [B013*{(23.0)//(37.0)}*{(24)}*{(24)}]///"
            "39: [B008*{(14.0)}*{(22)}*{(22)}]///"
            "40: [D000***]///"
            "41: [N000**{(33)}*]///"
            "129: [A000***]"
        )
        self.game.send_update = lambda b: self.broadcast(b.encode())

        # Configuring Events

        # self.connect_client_event += lambda client: if self.game: self.game.connect(client)
        # self.terminate_client_event += lambda client, *args, **kwargs: self.disconnect_from_game(b"", client)
        # self.terminate_client_event += lambda client, *args, **kwargs: self.log_out(b"", client, kicked=True)

        # Starting self

        self.start()

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
            try: self.broadcast(input("").encode())
            except (UnicodeDecodeError, KeyboardInterrupt):
                self.shut_down()

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
        self.game.display()
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
