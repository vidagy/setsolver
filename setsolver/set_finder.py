from itertools import combinations
from typing import List, TypeVar

from setsolver.board import Board
from setsolver.card import Card, GameSet


def find_all_sets(board: Board) -> List[GameSet]:
    sets: List[GameSet] = []
    for cards in combinations(board.cards, 3):
        if is_set(*cards):
            sets.append(GameSet(cards=set(cards)))
    return sets


T = TypeVar("T")


def is_same_or_all_different(a: T, b: T, c: T) -> bool:
    is_same = a == b and b == c
    if is_same:
        return True
    is_different = a != b and b != c and a != c
    if is_different:
        return True
    return False


def is_set(a: Card, b: Card, c: Card) -> bool:
    is_it_a_set = is_same_or_all_different(a.fill, b.fill, c.fill)
    if not is_it_a_set:
        return False
    is_it_a_set = is_same_or_all_different(a.color, b.color, c.color)
    if not is_it_a_set:
        return False
    is_it_a_set = is_same_or_all_different(a.count, b.count, c.count)
    if not is_it_a_set:
        return False
    is_it_a_set = is_same_or_all_different(a.shape, b.shape, c.shape)
    return is_it_a_set
