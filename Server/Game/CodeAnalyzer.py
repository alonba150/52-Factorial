from typing import List

from Utils.Event import Event


class CodeAnalyzer:
    def __init__(self, game):
        self.game = game
        self.__initialize_commands()

    def analyze_code(self, code: str):
        self.nodes = {}
        self.starter_nodes = []

        if not code: return lambda: None
        if not self.__initialize_nodes(list(map(lambda c: c.split(': '), code.split('///'))), self.__find_dict):
            print('BAD')
            return lambda: None
        for node in self.nodes.values():
            print(node)

        events = [Event(), Event(), Event()]
        for node in self.starter_nodes:
            for event in events: event += node
        for node in self.nodes.values():
            if node.type == "E":
                events[node.type_index] += node
                print('SUCCESS')

        events[1] += self.__clear_all_nodes

        return events

    def __clear_all_nodes(self):
        for node in self.nodes.values(): node.clear()

    def __initialize_nodes(self, nodes_data: List[str], func_dict: dict) -> bool:
        """
        Manages all the nodes accordingly to create a functioning web of them
        :param nodes_data: string list containing id and data for each node
        :param func_dict: a dict containing all the command functions
        """
        self.func_dict = func_dict
        nodes = []
        for node_data in nodes_data:
            if not type(node_data) is list or not len(node_data) == 2: return False
            nodes.append(Node(node_data[0], self))
        if not all(nodes[node_i].set_attr(nodes_data[node_i][1]) for node_i in range(len(nodes))):
            print("Bad Attr")
            return False
        if not all(node.initialize_connections() for node in nodes):
            print('Bad Conn')
            return False
        for node in list(self.nodes.values()):
            node.static
            node.repeatable
        return True

    def __initialize_commands(self):
        # region THE BIG SWITCH CASE

        # A type
        self.__info_nodes = {
            0: (self.game.get_players_command, 0),
            1: (self.game.get_bundles_command, 0),
            2: (self.game.get_player_turn, 0),
            3: (self.game.get_active_player, 0),
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
            7: (self.game.equals_command, 2),
            8: (self.game.get_bundle_command, 1),
            9: (self.game.range_command, 2),
        }

        # C type
        self.__command_nodes = {
            0: (self.game.foreach_command, 1),
            1: (self.game.give_cards_command, 2),
            2: (self.game.split_stack_between_players, 1),
            3: (self.game.move, 3),
            4: (self.game.practice_war, 1),
        }

        # D type
        self.__special_nodes = {
            0: (self.game.finish_turn, 0),
            1: (self.game.branch, 1)
        }

        # N type
        self.__numbers = {
            0: ((lambda: {0: [0]}), 0),
            1: ((lambda: {0: [1]}), 0),
            2: ((lambda: {0: [2]}), 0),
            3: ((lambda: {0: [3]}), 0),
            4: ((lambda: {0: [4]}), 0),
            5: ((lambda: {0: [5]}), 0),
            6: ((lambda: {0: [6]}), 0),
            7: ((lambda: {0: [7]}), 0),
            8: ((lambda: {0: [8]}), 0),
            9: ((lambda: {0: [9]}), 0),
            10: ((lambda: {0: [10]}), 0),
        }

        self.__find_dict = {
            'A': self.__info_nodes,
            'B': self.__sub_command_nodes,
            'C': self.__command_nodes,
            'D': self.__special_nodes,
            'N': self.__numbers
        }

        # endregion


class Node:

    def __init__(self, node_id, game):
        self.__id = node_id
        self.__game = game
        # Adds self to the dict of nodes by ids
        game.nodes[self.id] = self

        self.__func = None
        self.__inputs = []
        self.__outputs = []
        self.__triggers = []
        self.__static = None
        self.__type = None
        self.__type_index = None
        self.__repeatable = None
        self.__repeating = False

    @property
    def id(self) -> int:
        return self.__id

    @property
    def func(self):
        return self.__func

    @property
    def static(self):
        if self.__static is not None:
            return self.__static
        self.__static = bool((
                                     not self.__inputs or
                                     all(any(input_node[0].static for input_node in input_slot) for input_slot in
                                         self.__inputs)
                             ) and self.__type != "C" and self.__type != "D"
                             )
        return self.__static

    @property
    def repeatable(self):
        if self.__repeatable is not None:
            return self.__repeatable
        self.__repeatable = bool(self.__repeatable or \
                                 any(any(input_node[0].repeatable for input_node in input_slot) for input_slot in
                                     self.__inputs))
        return self.__repeatable

    @property
    def repeating(self):
        return self.__repeating

    @property
    def type(self):
        return self.__type

    @property
    def type_index(self):
        return self.__type_index

    def set_attr(self, data) -> bool:
        """
        Changes this node's data from a string containing both it's id
        and other information
        :param data: string containing the information
        :return: function success boolean
        """
        try:
            # Reads data from string with some string manipulation
            func_code, inputs, outputs, triggers = data[1:-1].split('*')  # Removing brackets [] and splitting
            self.__type = func_code[0]  # Setting the type (FE: 'A' or 'C')
            if self.__type == 'A' or self.__type == 'N': self.__game.starter_nodes.append(self)
            self.__type_index = int(func_code[1:4])
            # Get function from string code (FE: A000)
            if self.__type != 'E':
                self.__func = self.__game.func_dict[self.__type][self.__type_index]
            else:
                self.__func = (lambda: None, 0)
            if func_code[0:4] == "C000":
                self.__repeatable = True
                self.__repeating = True
            if inputs:  # Parse inputs -> List[List[(node_ID, node_output_slot_index)]]
                self.__inputs = list(map(
                    lambda input_slot: list(map(
                        lambda input_node: tuple(input_node.split('.')), input_slot[1:-1].split('/')
                    )),
                    inputs[1:-1].split('//')
                ))
            if outputs:  # Parse outputs List[Dict<node_ID, List[]>]
                self.__outputs = list(map(
                    lambda output_nodes: {output_node: [] for output_node in output_nodes[1:-1].split('/')},
                    outputs[1:-1].split('//')
                ))

            if triggers:  # Parse triggers List[List[node_ID]]
                self.__triggers = list(map(
                    lambda trigger_slot: trigger_slot[1:-1].split('/'),
                    triggers[1:-1].split('//')
                ))

            return True  # Function Succeeded

        except ValueError:
            return False

    def initialize_connections(self) -> bool:
        """
        `1
        :return: function success boolean
        """
        for slot_index in range(len(self.__inputs)):
            for input_node_index in range(len(self.__inputs[slot_index])):
                if not (node := self.__game.nodes.get(self.__inputs[slot_index][input_node_index][0], False)):
                    return False
                self.__inputs[slot_index][input_node_index] = node, self.__inputs[slot_index][input_node_index][1]
        for slot_index in range(len(self.__outputs)):
            keys = list(self.__outputs[slot_index].keys())
            for output_node_id in keys:
                if not (node := self.__game.nodes.get(output_node_id, False)):
                    return False
                self.__outputs[slot_index][node] = []
            for output_node_id in keys:
                self.__outputs[slot_index].pop(output_node_id, None)
        for trigger_slot_index in range(len(self.__triggers)):
            for node_index in range(len(self.__triggers[trigger_slot_index])):
                if not (node := self.__game.nodes.get(self.__triggers[trigger_slot_index][node_index], False)):
                    # print(self)
                    return False
                self.__triggers[trigger_slot_index][node_index] = node
        return True

    def has_value(self, node_sender, output_index):
        if output_index >= len(self.__outputs) or not \
                (res := self.__outputs[output_index].get(node_sender, None)):
            return False
        return res

    def pop_value(self, node_sender, output_index):
        if output_index >= len(self.__outputs) or not (res := self.__outputs[output_index].get(node_sender, False)):
            return False
        if len(res) > 0:
            return res[0] \
                if self.static and not node_sender.repeating else \
                self.__outputs[output_index][node_sender].pop(0)
        return False

    def __get_values(self):
        ret = []
        for input_slot in self.__inputs:
            for input_node in input_slot:
                if input_node[0].has_value(self, int(input_node[1])):
                    ret.append(input_node[0].pop_value(self, int(input_node[1])))
                    break
        return ret

    def __call__(self, *args, **kwargs):
        print(self.__type, self.__type_index, self.id)
        if not all(
                any(
                    input_node[0].has_value(self, int(input_node[1])) for input_node in input_slot
                ) for input_slot in self.__inputs
        ):
            if self.__type == "C": all(
                all(
                    print(input_node[0].has_value(self, int(input_node[1]))) for input_node in input_slot
                ) for input_slot in self.__inputs
        )
            return

        if results := self.func[0](*self.__get_values()):
            if type(results) is not tuple: results = results, []
            if len(results) == 2 and type(results[0]) is dict:
                for i in range(len(self.__outputs)):
                    if res := results[0].get(i, False):
                        for output in self.__outputs[i].keys():
                            if type(res) is list:
                                self.__outputs[i][output].extend(res)
                            else:
                                self.__outputs[i][output].append(res)
                if results[1] and type(results[1]) is tuple:
                    for res in results[1]:
                        if type(res) is int and res < len(self.__triggers):
                            for trigger in self.__triggers[res]:
                                trigger()
        if len(self.__triggers) == 1:
            for trigger in self.__triggers[0]:
                trigger()
        if self.__type:
            for output_slot in self.__outputs:
                for output in output_slot.keys():
                    if output.static:
                        output()
        if not self.static and self.repeatable and self.type != 'D':
            print('CALLED SELF')
            self()

    def clear(self):
        for i in range(len(self.__outputs)):
            for output in self.__outputs[i].keys():
                self.__outputs[i][output] = []

    def __str__(self):
        return f"\rNode ({self.__id}):\n\r\t{self.func=}\n\r\tinput={self.__inputs[0][0][0].id if self.__inputs else ''}" \
               f"\n\r\toutput={list(self.__outputs[0].keys())[0].id if self.__outputs else ''}\n\r\t{self.static=}" \
               f"\n\r\tself.__triggers=" \
               f"{self.__triggers[0].id if self.__triggers and type(self.__triggers[0]) is Node else '[]'}\n\r\n\r"
