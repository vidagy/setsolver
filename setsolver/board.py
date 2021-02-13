from dataclasses import dataclass
from typing import Set

from setsolver.card import Card


@dataclass
class Board:
    cards: Set[Card]

    @property
    def number_of_cards(self) -> int:
        return len(self.cards)

    def __post_init__(self) -> None:
        if len(self.cards) % 3 != 0:
            raise RuntimeError("Board should be divisible by 3, looser")
