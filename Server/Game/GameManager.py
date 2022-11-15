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

        self.bundles = [Bundle(), Bundle(), Bundle(), Bundle()]

        self.__analyzer = CodeAnalyzer(self)
        self.start = self.__analyzer.analyze_code(code)
        self.start()
        print(self.players)
        print(self.bundles)

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

    def get_players_command(self, next_command):
        print("A0")
        next_command(self.players)

    def get_bundles_command(self, next_command):
        print("A1")
        next_command(self.bundles)

    # endregion

    # region B Commands
    def get_bundle_by_player_command(self, player, next_command):
        print("B0")
        next_command(self.bundles[self.players.index(player)])

    @staticmethod
    def count_command(lst: list, next_command):
        print("B1")
        next_command(len(lst))

    @staticmethod
    def number_command(num: str, next_command):
        print("B2")
        next_command(int(num))

    @staticmethod
    def add_command(n1: int, n2: int, next_command):
        print("B3")
        next_command(n1 + n2)

    @staticmethod
    def subtract_command(n1: int, n2: int, next_command):
        print("B4")
        next_command(n1 - n2)

    @staticmethod
    def multiply_command(n1: int, n2: int, next_command):
        print("B5")
        next_command(n1 * n2)

    @staticmethod
    def divide_command(n1: int, n2: int, next_command):
        print("B6")
        next_command(n1 // n2)

    # endregion

    # region C Commands
    @staticmethod
    def foreach_command(lst: list, next_command):
        print("C1")
        for item in lst: next_command(item)

    @staticmethod
    def give_cards_command(b: Bundle, count: int, next_command):
        print("C2")
        for _ in range(count): b.append(Card(random.randint(0, 3), random.randint(0, 12)))
        next_command()

    # endregion

    def start(self):
        pass

    def next(self, move):
        pass


if __name__ == '__main__':
    g = Game("C001(B004(C000(A000)),B003(B006(52),B005(A000)))")
