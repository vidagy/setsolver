from dataclasses import dataclass
from typing import Set

from setsolver.properties import Color, Count, Fill, Shape


@dataclass(frozen=True, unsafe_hash=True)
class Card:
    """
    Represents a Card of the Set game.
    """

    fill: Fill
    count: Count
    color: Color
    shape: Shape


@dataclass(frozen=True, unsafe_hash=True)
class GameSet:
    """
    Represents three cards that are a Set.
    """

    cards: Set[Card]

    def __post_init__(self) -> None:
        if len(self.cards) != 3:
            raise RuntimeError("GameSet must consist of 3 cards, looser")
