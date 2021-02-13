from enum import Enum


class Fill(str, Enum):
    EMPTY = "empty"
    STRIPED = "striped"
    FULL = "full"

    def __repr__(self) -> str:
        return self.value


class Count(str, Enum):
    ONE = "one"
    TWO = "two"
    THREE = "three"

    def __repr__(self) -> str:
        return self.value


class Color(str, Enum):
    RED = "red"
    GREEN = "green"
    PURPLE = "purple"

    def __repr__(self) -> str:
        return self.value


class Shape(str, Enum):
    DIAMOND = "diamond"
    OVAL = "oval"
    WAVE = "wave"

    def __repr__(self) -> str:
        return self.value
