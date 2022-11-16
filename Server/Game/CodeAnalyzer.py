from typing import List

from Utils.Event import Event


class CodeAnalyzer:
    def __init__(self, game):
        self.game = game
        self.__initialize_commands()

    def analyze_code(self, code: str):
        Node.initialize_nodes(list(map(lambda c: c.split(': '), code.split('///'))), self.__find_dict)

    def __initialize_commands(self):
        # region THE BIG SWITCH CASE

        # A type
        self.__info_nodes = {
            0: (self.game.get_players_command, 0),
            1: (self.game.get_bundles_command, 0),
        }

        # B type
        self.__sub_command_nodes = {
            0: (self.game.add_command, 2),
            1: (self.game.subtract_command, 2),
            2: (self.game.multiply_command, 2),
            3: (self.game.divide_command, 2),
            4: (self.game.get_bundle_by_player_command, 1),
            5: (self.game.count_command, 1),
            6: (self.game.number_command, 1),
        }

        # C type
        self.__command_nodes = {
            0: (self.game.foreach_command, 1),
            1: (self.game.give_cards_command, 2),
        }

        self.__find_dict = {
            'A': self.__info_nodes,
            'B': self.__sub_command_nodes,
            'C': self.__command_nodes
        }

        # endregion


class Node:
    nodes = {}
    starter_nodes = []
    func_dict = {}

    @staticmethod
    def initialize_nodes(nodes_data: List[str], func_dict: dict):
        """
        Manages all the nodes accordingly to create a functioning web of them
        :param nodes_data: string list containing id and data for each node
        :param func_dict: a dict containing all the command functions
        """
        Node.func_dict = func_dict
        nodes = []
        for node_data in nodes_data: nodes.append(Node(node_data[0]))
        for node_i in range(len(nodes)): nodes[node_i].set_attr(nodes_data[node_i])
        for node in Node.nodes.values(): node.do_static()

    def __init__(self, node_id):
        self.__id = node_id
        # Adds self to the dict of nodes by ids
        Node.nodes[self.id] = self

        self.__func = None
        self.__inputs = []
        self.__outputs = []
        self.static = 0

    @property
    def id(self) -> int:
        return self.__id

    @property
    def func(self):
        return self.__func

    def set_attr(self, data: str) -> bool:
        """
        Changes this node's data from a string containing both it's id
        and other information
        :param data: string containing the information
        :return: function success boolean
        """
        if data.count(': ') != 1: return False
        self.__id, node_data = data.split(': ')
        # Reads data from string with some string manipulation
        node_data = node_data[1:-1]  # Removing brackets []
        func_code, inputs, outputs = node_data.split('*')
        self.__func = Node.func_dict[func_code[0]][int(func_code[1])]  # Get function from string code (FE: A000)

        # Add node as starter node if node is type A

    def initialize_connections(self) -> bool:
        pass

    def has_value(self, output_index):
        if output_index >= len(self.__outputs):
            return False
        return self.__outputs[output_index]

    def pop_value(self, output_index):
        if output_index >= len(self.__outputs):
            return False
        if len(self.__outputs[output_index]) > 0:
            return self.__outputs[0] if self.static else self.__outputs.pop(0)
        return False

    def do_static(self):
        self.static = all(input_node[0].static for input_node in self.__inputs)

    def __call__(self, *args, **kwargs):
        if all(input_node[0].has_value(input_node[1]) for input_node in self.__inputs):
            self.func(*[input_node[0].pop_value(input_node[1]) for input_node in self.__inputs])
