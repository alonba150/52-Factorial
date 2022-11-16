from socket import socket
from Game.GameObjects.Bundle import *
from Game.GameObjects.Card import *
from Game.CodeAnalyzer import CodeAnalyzer
import random


class Game:
    players: List[socket] = [1, 2, 3, 4]
    player_turn: socket = None
    player_count: int = 0
    can_start: bool = False

    bundles: List[Bundle] = []

    def __init__(self, code: str):
        self.player_count = 4
        # self.bundles = [Bundle([Card(1, 0), Card(2, 2), Card(3, 9), Card(0, 12)]),
        #                Bundle([Card(0, 2), Card(3, 9), Card(1, 1), Card(2, 0)]),
        #                Bundle([Card(2, 7), Card(1, 0), Card(0, 12), Card(1, 10)]),
        #                Bundle([Card(3, 4), Card(0, 7), Card(2, 5), Card(3, 3)]),
        #                Bundle([])]

        self.bundles = [Bundle(cards=[]), Bundle(cards=[]), Bundle(cards=[]), Bundle(cards=[])]

        self.__analyzer = CodeAnalyzer(self)
        self.start = self.__analyzer.analyze_code(code)
        self.start()
        print(self.players)
        print(*self.bundles, sep='\n')

    def connect(self, sock: socket):
        if sock in self.players:
            return False
        if len(self.players) >= self.player_count:
            return False
        self.players.append(sock)
        self.can_start = True
        return True

    def disconnect(self, sock: socket):
        if sock not in self.players:
            return False
        self.players.remove(sock)
        self.can_start = False
        return True

    # region A Commands

    def get_players_command(self, next_command, static=True):
        print("A0")
        next_command(self.players)

    def get_bundles_command(self, next_command, static=True):
        print("A1")
        next_command(self.bundles)

    # endregion

    # region B Commands
    def get_bundle_by_player_command(self, player, next_command, static=True):
        print("B4")
        next_command(self.bundles[self.players.index(player)], static=static)

    @staticmethod
    def count_command(lst: list, next_command, static=True):
        print("B5")
        next_command(len(lst), static=static)

    @staticmethod
    def number_command(num: str, next_command, static=True):
        print("B6")
        next_command(int(num), static=static)

    @staticmethod
    def add_command(n1: int, n2: int, next_command, static=True):
        print("B0")
        next_command(n1 + n2, static=static)

    @staticmethod
    def subtract_command(n1: int, n2: int, next_command, static=True):
        print("B1")
        next_command(n1 - n2, static=static)

    @staticmethod
    def multiply_command(n1: int, n2: int, next_command, static=True):
        print("B2")
        next_command(n1 * n2, static=static)

    @staticmethod
    def divide_command(n1: int, n2: int, next_command, static=True):
        print("B3")
        next_command(n2 // n1, static=static)

    # endregion

    # region C Commands
    @staticmethod
    def foreach_command(lst: list, next_command, static=None):
        print("C0")
        for item in lst: next_command(item, static=False)

    @staticmethod
    def give_cards_command(b: Bundle, count: int, next_command, static=True):
        print("C1")
        print(f"{b=}")
        print(f"{count=}")
        for _ in range(count): b.append(Card(random.randint(0, 3), random.randint(0, 12)))
        next_command(static=static)

    # endregion

    def start(self):
        pass

    def next(self, move):
        pass


if __name__ == '__main__':
    g = Game("C001(B004(C000(A000)),B003(52,B005(A000)))")
