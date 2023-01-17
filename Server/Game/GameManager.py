from socket import socket
from Game.GameObjects.Bundle import *
from Game.GameObjects.Card import *
from Game.CodeAnalyzer import CodeAnalyzer
import random
from Utils.Event import Event


class Game:

    def __init__(self, code: str, code_turn: str, players=[], player_count=4):
        self.players: List[socket] = players
        self.player_count: int = player_count
        self.can_start: bool = False
        self.bundles: List[Bundle] = []

        # self.bundles = [Bundle([Card(1, 0), Card(2, 2), Card(3, , 1), Card(2, 0)]),
        #         #                Bundle([Card(2, 7), Card(1, 0), Card(9), Card(0, 12)]),
        #                Bundle([Card(0, 2), Card(3, 9), Card(10, 12), Card(1, 10)]),
        #                Bundle([Card(3, 4), Card(0, 7), Card(2, 5), Card(3, 3)]),
        #                Bundle([])]

        self.bundles = [Bundle(cards=[]) for _ in range(player_count * 3)]

        self.send_update = Event()

        self.codes = code, code_turn

        self.player_turn = None
        self.player_turn_index = None
        self.current_player = None
        self.current_player_index = None
        self.current_selected_cards = None
        # self.display()

    def connect(self, sock: socket):
        if sock in self.players:
            return False
        if len(self.players) >= self.player_count:
            return False
        self.players.append(sock)
        if len(self.players) == self.player_count:
            self.can_start = True
            self.player_turn = self.players[0]
            self.player_turn_index = 0
            self.__analyzer = CodeAnalyzer(self)
            self.__analyzer1 = CodeAnalyzer(self)
            self.start, self.do_turn, self.end = self.__analyzer.analyze_code(self.codes[0])
            # print(self.__analyzer.nodes['6'].repeatable)
            _, self.do_turn, _ = self.__analyzer1.analyze_code(self.codes[1])
            self.start()
        return True

    def disconnect(self, sock: socket):
        print('\n DISCONNECT \n')
        if sock not in self.players:
            return False
        self.players.remove(sock)
        self.can_start = False
        return True

    # region A Commands

    def get_players_command(self):
        print("A0")
        return {0: [self.players.copy()]}

    def get_bundles_command(self):
        print("A1")
        return {0: [self.bundles.copy()]}

    def get_active_player(self):
        print("A2")
        return {0: [self.current_player_index]}

    def get_player_turn(self):
        print("A3")
        return {0: [self.player_turn_index]}

    # endregion

    # region B Commands
    def get_bundle_by_player_command(self, player):
        print("B4")
        print(player, self.players)
        return {0: [self.bundles[self.players.index(player)]]}

    def get_card_command(self, bundle, index):
        return {0: [bundle.cards[index]]}

    def get_value_commande(self, card):
        return card.value

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

    @staticmethod
    def equals_command(t1, t2):
        return {0: [t1 == t2]}

    def get_bundle_command(self, index):
        return {0: [self.bundles[index]]}

    @staticmethod
    def range_command(start, end):
        return {0: [[*range(start, end)]]}

    # endregion

    # region C Commands
    @staticmethod
    def foreach_command(lst: list):
        print("C0")
        return {0: lst}

    @staticmethod
    def give_cards_command(b: Bundle, count: int):
        for _ in range(count): b.append(Card(random.randint(0, 3), random.randint(0, 12)))

    def split_stack_between_players(self, each_player_card_count: int):
        if each_player_card_count * self.player_count > 52: return
        deck = Bundle.create_deck().shuffle()
        for b in self.bundles[:self.player_count]:
            for _ in range(each_player_card_count): deck.move(b, 0)

    def move(self, b, other, index: int):
        b.move(other, index)

    def practice_war(self, r):
        print("WAR")
        _max = -1
        index = -1
        for i in r:
            if self.bundles[i + 4].cards[0].value > _max:
                _max = self.bundles[i + 4].cards[0].value
                index = i
        for i in r:
            self.bundles[i + 4].move(self.bundles[index + 8], 0)

    # endregion

    # region D Commands

    def finish_turn(self):
        self.player_turn_index = (self.player_turn_index + 1) % self.player_count
        self.player_turn = self.players[self.player_turn_index]
        self.send_update(self.bundles.__str__())
        print('\n\nTURN OVER\n\n')

    def branch(self, bool):
        # print('BRANCH ' + ('true' if bool else 'false'))
        if bool: return {}, (0,)
        return {}, (1,)

    # endregion

    def activate(self, player, selected_cards=[]):
        if not self.can_start: return
        self.current_player = player
        self.current_player_index = self.players.index(self.current_player)
        self.current_selected_cards = selected_cards
        self.do_turn()

    def get_game_str(self):
        return self.bundles

    def display(self):
        print(self.players)
        print(*self.bundles, sep='\n')


if __name__ == '__main__':
    # g = Game("C001(B004(C000(A000)),B003(52,B005(A000)))")
    # Iteration 1
    # g = Game("0: [A000**{(1/2)}*]///1: [C000*{(0.0)}*{(5)}*{(5)}]///2: [B005*{(0.0)}*{(4)}*]///3: [A000**{(4)}*]///"
    #          "4: [B003*{(3.0)//(2.0)}*{(6)}*]///5: [B004*{(1.0)}*{(6)}*{(6)}]///6: [C001*{(5.0)//(4.0)}**]///"
    #          "7: [E000***{(1)}]")
    # Iteration 2
    g = Game("0: [A000**{(1/2)}*]///1: [C000*{(0.0)}*{(5)}*{(5)}]///2: [B005*{(0.0)}*{(4)}*]///3: [A000**{(4)}*]///"
             "4: [B003*{(3.0)//(2.0)}*{(6)}*]///5: [B004*{(1.0)}*{(6)}*{(6)}]///6: [C001*{(5.0)//(4.0)}**]///"
             "7: [E000***{(1)}]",
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
             "10: [B009*{(18.0)//(19.0)}*{(14)}*]///"
             "11: [D001*{(12.0)}**{(14)//(16)}]///"
             "12: [B007*{(13.0)//(20.0)}*{(11)}*]///"
             "13: [A003**{(12)}*]///"
             "14: [C004*{(10.0)}**{(16)}]///"
             "15: [N000**{(2)}*]///"
             "16: [D000***]///"
             "17: [N004**{(8)}*]///"
             "18: [N000**{(10)}*]///"
             "19: [N004**{(10)}*]///"
             "20: [N003**{(12)}*]///"
             "129: [A000***]"
             , players=[0, 1, 2, 3])
    while True:
        for i in range(52):
            input()
            g.activate(i % 4, [])
            print(g.player_turn, g.current_player, '\n\n')
            g.display()
        for i in range(8, 12):
            for _ in range(len(g.bundles[i].cards)):
                g.bundles[i].move(g.bundles[i - 8], 0)
