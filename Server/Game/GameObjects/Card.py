card_types = [i for i in range(0, 4)]
card_values = [i for i in range(0, 13)]


class Card:
    def __init__(self, ctype: int, value: int):
        self.type: int = ctype
        self.value: int = value
