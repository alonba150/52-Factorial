from Game.GameObjects.Card import *
from typing import List
import random


class Bundle:
    cards: List[Card] = []

    def __init__(self, cards: List[Card] = [], pos=(0.0, 0.0, 0.0)):
        self.cards = cards
        self.position = pos

    def __getitem__(self, item) -> Card:
        return self.cards[item]

    def __iter__(self) -> List[Card]:
        return self.cards

    def __add__(self, other):
        return Bundle(self.cards + other.cards)

    def pop(self, index) -> Card:
        return self.cards.pop(index)

    def append(self, card: Card):
        self.cards.append(card)
        return self

    def insert(self, index, card: Card):
        self.cards.insert(index, card)
        return self

    def move(self, other, index=0):
        if index >= len(self.cards): return
        return other.append(self.pop(index))

    @staticmethod
    def create_deck():
        b = Bundle()
        for i in card_types:
            for j in card_values:
                b.append(Card(i, j))
        return b

    def shuffle(self):
        random.shuffle(self.cards)
        return self

    def __repr__(self):
        return f"Bundle {len(self.cards)}: [{self.cards} + {self.position}]"

