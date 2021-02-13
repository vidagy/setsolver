from unittest import TestCase

from setsolver.board import Board
from setsolver.card import Card, GameSet
from setsolver.properties import Fill, Color, Count, Shape
from setsolver.set_finder import is_same_or_all_different, is_set, find_all_sets


class TestSetFinder(TestCase):
    card1 = Card(Fill.FULL, Count.ONE, Color.RED, Shape.OVAL)
    card2 = Card(Fill.STRIPED, Count.TWO, Color.PURPLE, Shape.OVAL)
    card3 = Card(Fill.EMPTY, Count.THREE, Color.GREEN, Shape.OVAL)
    card4 = Card(Fill.EMPTY, Count.THREE, Color.PURPLE, Shape.WAVE)
    card5 = Card(Fill.EMPTY, Count.THREE, Color.RED, Shape.DIAMOND)
    card6 = Card(Fill.EMPTY, Count.THREE, Color.PURPLE, Shape.DIAMOND)
    card7 = Card(Fill.STRIPED, Count.ONE, Color.RED, Shape.DIAMOND)
    card8 = Card(Fill.STRIPED, Count.TWO, Color.GREEN, Shape.DIAMOND)
    card9 = Card(Fill.FULL, Count.ONE, Color.GREEN, Shape.WAVE)
    card10 = Card(Fill.EMPTY, Count.ONE, Color.RED, Shape.DIAMOND)
    card11 = Card(Fill.FULL, Count.TWO, Color.GREEN, Shape.DIAMOND)
    card12 = Card(Fill.EMPTY, Count.ONE, Color.PURPLE, Shape.DIAMOND)

    def test_is_set(self):
        self.assertTrue(is_set(self.card1, self.card2, self.card3))

    def test_is_set_false(self):
        card1 = Card(Fill.FULL, Count.ONE, Color.GREEN, Shape.OVAL)
        card2 = Card(Fill.STRIPED, Count.TWO, Color.PURPLE, Shape.OVAL)
        card3 = Card(Fill.EMPTY, Count.THREE, Color.GREEN, Shape.OVAL)
        self.assertFalse(is_set(card1, card2, card3))

    def test_is_same_or_all_different_same(self):
        self.assertTrue(is_same_or_all_different(Fill.FULL, Fill.EMPTY, Fill.STRIPED))
        self.assertTrue(is_same_or_all_different(Count.ONE, Count.TWO, Count.THREE))
        self.assertTrue(is_same_or_all_different(Color.PURPLE, Color.RED, Color.GREEN))
        self.assertTrue(is_same_or_all_different(Shape.OVAL, Shape.WAVE, Shape.DIAMOND))

        for p in [Fill.FULL, Fill.EMPTY, Fill.STRIPED, Count.ONE, Count.TWO, Count.THREE, Color.PURPLE, Color.RED,
                  Color.GREEN, Shape.OVAL, Shape.WAVE, Shape.DIAMOND]:
            self.assertTrue(is_same_or_all_different(p, p, p))

    def test_find_all_sets(self):
        board = Board({self.card1, self.card2, self.card3, self.card4, self.card5, self.card6, self.card7, self.card8,
                       self.card9, self.card10, self.card11, self.card12})
        expected_sets = [
            GameSet({self.card1, self.card2, self.card3}),
            GameSet({self.card3, self.card4, self.card5}),
            GameSet({self.card3, self.card8, self.card9}),
            GameSet({self.card2, self.card5, self.card9}),
            GameSet({self.card1, self.card4, self.card8}),
            GameSet({self.card6, self.card7, self.card11}),
        ]
        self.assertCountEqual(expected_sets, find_all_sets(board))
