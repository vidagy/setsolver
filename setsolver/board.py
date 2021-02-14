from dataclasses import dataclass
from typing import Set

from setsolver.card import Card


@dataclass
class Board:
    """
    Represents the boards, that contains all cards dealt on the table.
    """

    cards: Set[Card]

    @property
    def number_of_cards(self) -> int:
        """
        Returns the number of cards on the Board.
        """
        return len(self.cards)

    def __post_init__(self) -> None:
        if len(self.cards) % 3 != 0:
            raise RuntimeError("Board should be divisible by 3, looser")
