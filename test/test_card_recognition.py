import os
import pickle
from unittest import TestCase

from setsolver.image_detection.card_recognition import CardRecognition

path = os.path.join(os.path.dirname(os.path.abspath(__file__)))


class TestSetFinder(TestCase):
    solutions_number5 = {
        0: 3,
        1: 1,
        2: 2,
        3: 1,
        4: 2,
        5: 1,
        6: 2,
        7: 2,
        8: 1,
        9: 1,
        10: 1,
        11: 3,
    }
    solutions_shape5 = {
        0: "diamond",
        1: "wave",
        2: "wave",
        3: "diamond",
        4: "diamond",
        5: "oval",
        6: "wave",
        7: "wave",
        8: "diamond",
        9: "diamond",
        10: "diamond",
        11: "oval",
    }
    solutions_number1 = {
        0: 2,
        1: 2,
        2: 2,
        3: 2,
        4: 3,
        5: 3,
        6: 2,
        7: 1,
        8: 1,
        9: 2,
        10: 1,
        11: 3,
    }
    solutions_shape1 = {
        0: "oval",
        1: "wave",
        2: "diamond",
        3: "diamond",
        4: "wave",
        5: "oval",
        6: "diamond",
        7: "wave",
        8: "wave",
        9: "wave",
        10: "diamond",
        11: "wave",
    }
    solutions_shape2 = {
        0: "diamond",
        1: "wave",
        2: "wave",
        3: "diamond",
        4: "oval",
        5: "wave",
        6: "diamond",
        7: "wave",
        8: "oval",
        9: "wave",
        10: "diamond",
        11: "diamond",
        12: "wave",
        13: "diamond",
        14: "diamond",
    }
    solutions_number2 = {
        0: 2,
        1: 3,
        2: 1,
        3: 3,
        4: 3,
        5: 2,
        6: 1,
        7: 1,
        8: 2,
        9: 3,
        10: 2,
        11: 2,
        12: 2,
        13: 1,
        14: 2,
    }
    solutions_fill5 = {
        0: "striped",
        1: "empty",
        2: "empty",
        3: "striped",
        4: "empty",
        5: "striped",
        6: "empty",
        7: "striped",
        8: "striped",
        9: "empty",
        10: "empty",
        11: "striped",
    }
    solutions_fill4 = {
        0: "empty",
        1: "striped",
        2: "striped",
        3: "empty",
        4: "striped",
        5: "full",
        6: "striped",
        7: "striped",
        8: "full",
        9: "full",
        10: "empty",
        11: "striped",
    }
    solutions_fill2 = {
        0: "full",
        1: "full",
        2: "full",
        3: "empty",
        4: "striped",
        5: "striped",
        6: "striped",
        7: "striped",
        8: "empty",
        9: "empty",
        10: "full",
        11: "striped",
        12: "full",
        13: "striped",
        14: "empty",
    }
    solutions_fill1 = {
        0: "empty",
        1: "full",
        2: "striped",
        3: "empty",
        4: "full",
        5: "striped",
        6: "full",
        7: "striped",
        8: "full",
        9: "striped",
        10: "striped",
        11: "empty",
    }
    solutions_color1 = {
        0: "purple",
        1: "red",
        2: "purple",
        3: "purple",
        4: "red",
        5: "red",
        6: "red",
        7: "purple",
        8: "green",
        9: "purple",
        10: "red",
        11: "green",
    }
    solutions_color5 = {
        0: "purple",
        1: "purple",
        2: "red",
        3: "green",
        4: "green",
        5: "red",
        6: "purple",
        7: "purple",
        8: "red",
        9: "green",
        10: "purple",
        11: "green",
    }
    solutions_color2 = {
        0: "green",
        1: "red",
        2: "green",
        3: "green",
        4: "red",
        5: "purple",
        6: "purple",
        7: "red",
        8: "purple",
        9: "green",
        10: "red",
        11: "purple",
    }

    solutions_shape4 = {
        0: "oval",
        1: "oval",
        2: "diamond",
        3: "diamond",
        4: "wave",
        5: "diamond",
        6: "oval",
        7: "oval",
        8: "diamond",
        9: "wave",
        10: "wave",
        11: "wave",
    }
    solutions_number4 = {
        0: 2,
        1: 1,
        2: 3,
        3: 3,
        4: 2,
        5: 2,
        6: 2,
        7: 3,
        8: 1,
        9: 1,
        10: 3,
        11: 2,
    }

    number_solutions = {
        1: solutions_number1,
        5: solutions_number5,
        2: solutions_number2,
        4: solutions_number4,
    }
    shape_solutions = {
        1: solutions_shape1,
        5: solutions_shape5,
        2: solutions_shape2,
    }
    solutions_fill = {
        1: solutions_fill1,
        5: solutions_fill5,
        2: solutions_fill2,
        4: solutions_fill4,
        3: solutions_fill2,
    }
    solutions_color = {
        5: solutions_color5,
        2: solutions_color2,
        1: solutions_color1,
        3: solutions_color2,
    }

    def test_get_numbers1(self):
        scenario = 1
        with open(
            os.path.join(path, f"set_board_cards_{scenario}.p"), "rb"
        ) as f:
            cards = pickle.load(f)
        for i, card in enumerate(cards):
            image = CardRecognition(card)
            num = image.get_number_of_shapes()
            self.assertEqual(self.number_solutions.get(scenario).get(i), num)

    def test_get_numbers2(self):
        scenario = 2
        with open(
            os.path.join(path, f"set_board_cards_{scenario}.p"), "rb"
        ) as f:
            cards = pickle.load(f)
        for i, card in enumerate(cards):
            image = CardRecognition(card)
            num = image.get_number_of_shapes()
            self.assertEqual(self.number_solutions.get(scenario).get(i), num)

    def test_get_numbers4(self):
        scenario = 4
        with open(
            os.path.join(path, f"set_board_cards_{scenario}.p"), "rb"
        ) as f:
            cards = pickle.load(f)
        for i, card in enumerate(cards):
            image = CardRecognition(card)
            num = image.get_number_of_shapes()
            self.assertEqual(self.number_solutions.get(scenario).get(i), num)

    def test_get_numbers5(self):
        scenario = 4
        with open(
            os.path.join(path, f"set_board_cards_{scenario}.p"), "rb"
        ) as f:
            cards = pickle.load(f)
        for i, card in enumerate(cards):
            image = CardRecognition(card)
            num = image.get_number_of_shapes()
            self.assertEqual(self.number_solutions.get(scenario).get(i), num)

    def test_get_shape(self):
        scenario = 1
        with open(
            os.path.join(path, f"set_board_cards_{scenario}.p"), "rb"
        ) as f:
            cards = pickle.load(f)
        for i, card in enumerate(cards):
            image = CardRecognition(card)
            image.get_number_of_shapes()
            shape = image.get_shape()
            print(str(i) + " " + shape)
            self.assertEqual(self.solutions_shape1.get(i), shape)

    def test_get_fill(self):
        scenario = 5
        with open(
            os.path.join(path, f"set_board_cards_{scenario}.p"), "rb"
        ) as f:
            cards = pickle.load(f)
        for i, card in enumerate(cards):
            image = CardRecognition(card)
            image.get_number_of_shapes()
            fill = image.get_fill()
            # cv2.imshow("card", card)
            # cv2.waitKey()
            self.assertEqual(self.solutions_fill.get(scenario).get(i), fill)

    def test_get_color(self):
        scenario = 1
        with open(
            os.path.join(path, f"set_board_cards_{scenario}.p"), "rb"
        ) as f:
            cards = pickle.load(f)
        for i, card in enumerate(cards):
            image = CardRecognition(card)
            color = image.get_color()
            self.assertEqual(self.solutions_color.get(scenario).get(i), color)
