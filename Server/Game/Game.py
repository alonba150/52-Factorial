from socket import socket
from typing import List
from Game.Bundle import *
from Game.Card import *
import random


class Game:
    players: List[socket] = []
    player_turn: socket = None
    player_count: int = 0
    can_start: bool = False

    bundles: List[Bundle] = []

    def __init__(self, code: str):
        self.player_count = 4
        #self.bundles = [Bundle([Card(1, 0), Card(2, 2), Card(3, 9), Card(0, 12)]),
        #                Bundle([Card(0, 2), Card(3, 9), Card(1, 1), Card(2, 0)]),
        #                Bundle([Card(2, 7), Card(1, 0), Card(0, 12), Card(1, 10)]),
        #                Bundle([Card(3, 4), Card(0, 7), Card(2, 5), Card(3, 3)]),
        #                Bundle([])]

        code = "C1(B4(C1(A0)),B3(B6(52),B5(A0)))"

        self.start = {

        }



    def analyze_code(self, code: str):
        pass

    def __initialize_commands(self):
        # region THE BIG SWITCH CASE

        # A type
        self.__info_nodes = {
            0: self.players,
            1: self.bundles,
        }

        # B type
        self.__sub_command_nodes = {
            0: self.add_command,
            1: self.subtract_command,
            2: self.multiply_command,
            3: self.divide_command,
            4: self.get_bundle_by_player_command,
            5: self.count_command,
            6: self.number_command,
        }

        # C type
        self.__command_nodes = {
            0: self.foreach_command,
            1: self.give_cards_command,
        }

        # endregion

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

    # endregion

    # region B Commands
    def get_bundle_by_player_command(self, player, next_command):
        next_command(self.bundles[self.players.index(player)])

    @staticmethod
    def count_command(lst: list, next_command):
        next_command(len(lst))

    @staticmethod
    def number_command(num: str, next_command):
        next_command(int(num))

    @staticmethod
    def add_command(n1: int, n2: int, next_command):
        next_command(n1 + n2)

    @staticmethod
    def subtract_command(n1: int, n2: int, next_command):
        next_command(n1 - n2)

    @staticmethod
    def multiply_command(n1: int, n2: int, next_command):
        next_command(n1 * n2)

    @staticmethod
    def divide_command(n1: int, n2: int, next_command):
        next_command(n1 // n2)

    # endregion

    # region C Commands
    def foreach_command(self, lst: list, next_command):
        for item in lst: next_command(item)

    def give_cards_command(self, b: Bundle, count: int):
        for _ in range(count): b.append(Card(random.randint(0, 3), random.randint(0, 12)))

    # endregion

    def start(self):
        pass

    def next(self, move):
        pass
