from Core.Server import Server, ServerCommand

import threading


class GameServer(Server):

    def __init__(self):
        super().__init__(encrypted=False, input_handler=None, name='Game Server', port=55555)

        # Adding all commands

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

        # Configuring Events

        ##self.terminate_client_event += lambda client, _, __: self.remove_client(client)

        # Setting up variables

        t = threading.Thread(target=self.get_input)
        t.start()

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
                    val = func(self, command, client, *args, **kwargs)
                    if not val:
                        self._client_messages[client].append(str(fail_message).encode())
                except Exception as exe:
                    self._client_messages[client].append(str(fail_message).encode())
                    print(exe)
                print(fail_message)

            return applicator

        return decorator

    def get_input(self):
        while 1:
            self.broadcast(input(" -> ").encode())

if __name__ == '__main__':
    GameServer()
