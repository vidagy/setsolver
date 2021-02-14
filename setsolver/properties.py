from enum import Enum


class Fill(str, Enum):
    """
    Filling of a Card.
    """
    EMPTY = "empty"
    STRIPED = "striped"
    FULL = "full"

    def __repr__(self) -> str:
        return str(self.value)


class Count(str, Enum):
    """
    Count of a Card.
    """
    ONE = "one"
    TWO = "two"
    THREE = "three"

    def __repr__(self) -> str:
        return str(self.value)


class Color(str, Enum):
    """
    Color of a Card.
    """
    RED = "red"
    GREEN = "green"
    PURPLE = "purple"

    def __repr__(self) -> str:
        return str(self.value)


class Shape(str, Enum):
    """
    Shape of a Card.
    """
    DIAMOND = "diamond"
    OVAL = "oval"
    WAVE = "wave"

    def __repr__(self) -> str:
        return str(self.value)
