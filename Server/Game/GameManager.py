from socket import socket
from Game.GameObjects.Bundle import *
from Game.GameObjects.Card import *
from Game.CodeAnalyzer import CodeAnalyzer
import random


class Game:

    def __init__(self, code: str, players=[1, 2, 3, 4], player_count=4):
        self.players: List[socket] = players
        self.player_count: int = player_count
        self.can_start: bool = False
        self.bundles: List[Bundle] = []

        # self.bundles = [Bundle([Card(1, 0), Card(2, 2), Card(3, 9), Card(0, 12)]),
        #                Bundle([Card(0, 2), Card(3, 9), Card(1, 1), Card(2, 0)]),
        #                Bundle([Card(2, 7), Card(1, 0), Card(0, 12), Card(1, 10)]),
        #                Bundle([Card(3, 4), Card(0, 7), Card(2, 5), Card(3, 3)]),
        #                Bundle([])]

        self.bundles = [Bundle(cards=[]) for _ in self.players]

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

    def get_players_command(self):
        print("A0")
        return {0: [self.players]}

    def get_bundles_command(self):
        print("A1")
        return {0: [self.bundles]}

    # endregion

    # region B Commands
    def get_bundle_by_player_command(self, player):
        print("B4")
        return {0: [self.bundles[self.players.index(player)]]}

    @staticmethod
    def count_command(lst: list):
        print("B5")
        return {0: [len(lst)]}

    @staticmethod
    def number_command(num: str):
        print("B6")
        return {0: [int(num)]}

    @staticmethod
    def add_command(n1: int, n2: int):
        print("B0")
        return {0: [n1 + n2]}

    @staticmethod
    def subtract_command(n1: int, n2: int):
        print("B1")
        return {0: [n1 - n2]}

    @staticmethod
    def multiply_command(n1: int, n2: int):
        print("B2")
        return {0: [n1 * n2]}

    @staticmethod
    def divide_command(n1: int, n2: int):
        print("B3")
        return {0: [52 // n2]}

    # endregion

    # region C Commands
    @staticmethod
    def foreach_command(lst: list):
        print("C0")
        return {0: lst}

    @staticmethod
    def give_cards_command(b: Bundle, count: int):
        print("C1")
        print(f"{b=}")
        print(f"{count=}")
        for _ in range(count): b.append(Card(random.randint(0, 3), random.randint(0, 12)))

    # endregion

    def start(self):
        pass

    def next(self, move):
        pass


if __name__ == '__main__':
    # g = Game("C001(B004(C000(A000)),B003(52,B005(A000)))")
    g = Game("0: [A000**{(1/2)}*]///1: [C000*{(0.0)}*{(5)}*{(5)}]///2: [B005*{(0.0)}*{(4)}*]///3: [A000**{(4)}*]///"
             "4: [B003*{(3.0)//(2.0)}*{(6)}*]///5: [B004*{(1.0)}*{(6)}*{(6)}]///6: [C001*{(5.0)//(4.0)}**]///"
             "7: [E000***{(1)}]")
