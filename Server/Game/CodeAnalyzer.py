from Utils.Event import Event


class CodeAnalyzer:
    def __init__(self, game):
        self.game = game
        self.__initialize_commands()

    def read_code(self, code: str, node_next=(lambda *args, **kwargs: None)):
        if code.isdigit():
            return [Node(lambda _node_next, *args, **kwargs: _node_next(int(code)), 0, node_next)]
        cmd_t = code[0]
        cmd_i = code[1] + code[2] + code[3]
        node = Node(*self.__find_dict[cmd_t][int(cmd_i)], node_next)
        cmds = code[5:-1]
        if not cmds:
            return [node]
        starter_i = 0
        for index in [i for i, c in enumerate(cmds) if c == ',']:
            temp = cmds[starter_i: index]
            if temp.count('(') == temp.count(')'):
                starter_i = index
                cmds = cmds[0: index] + '%' + cmds[index+1:]
        cmds = cmds.split('%')
        print(cmds)
        results = []
        for sub_cmd in cmds:
            if res := self.read_code(sub_cmd, node): results.extend(res)
        return results

    def analyze_code(self, code: str):
        activate = Event()
        i = 0
        for node in self.read_code(code):
            if i >= 0:
                print(node)
                activate += node
            i += 1
        return activate

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
    def __init__(self, cmd, arg_l: int, node_next):
        self.cmd = cmd
        self.arg_l = arg_l
        self.args = []
        self.repeatables = []
        self.node_next = node_next

    def __call__(self, *args, static=True):
        #print(self)
        if not static:
            self.repeatables.append(args[0])
            if 1 + len(self.args) == self.arg_l:
                for arg in self.repeatables:
                    self.cmd(*([arg] + self.args), self.node_next, static=static)
                    self.repeatables.remove(arg)
        elif len(args) == self.arg_l:
            self.cmd(*args, self.node_next, static=static)
        elif len(args) == 1:
            self.args.append(args[0])
            if len(self.args) == self.arg_l:
                self.cmd(self.args[1], self.args[0], self.node_next, static=static)
            elif 1 + len(self.args) == self.arg_l:
                for arg in self.repeatables:
                    self.cmd(*([arg] + self.args), self.node_next, static=static)

    def __repr__(self):
        return \
            f"""Node:
    {self.cmd =}
    {self.arg_l =}
    {self.args =}
    {self.repeatables =}
"""

