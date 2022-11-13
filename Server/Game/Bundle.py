from Game.Card import *
from typing import List


class Bundle:
    cards: List[Card] = []

    def __init__(self, cards: List[Card]):
        self.cards = cards

    def __getitem__(self, item) -> Card:
        return self.cards[item]

    def __iter__(self) -> List[Card]:
        return self.cards

    def __add__(self, other):
        return Bundle(self.cards + other.cards)

    def pop(self, index) -> Card:
        return self.cards.pop(index)

    def append(self, card: Card):
        return self.cards.append(card)

    def insert(self, index, card: Card):
        return self.cards.insert(index, card)

    def move(self, other, index=0):
        other + self.pop(index)

