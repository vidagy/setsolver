from typing import Set
from dataclasses import dataclass

from setsolver.properties import Fill, Count, Color, Shape


@dataclass(frozen=True, unsafe_hash=True)
class Card:
    fill: Fill
    count: Count
    color: Color
    shape: Shape


@dataclass(frozen=True, unsafe_hash=True)
class GameSet:
    cards: Set[Card]

    def __post_init__(self):
        if len(self.cards) != 3:
            raise RuntimeError("GameSet must consist of 3 cards, looser")
