import os
import pickle
from unittest import TestCase

from setsolver.image_detection.board_recognition import BoardRecognition

path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "setsolver",
    "image_detection",
    "board_input",
)
board_cards = {0: 12, 1: 12, 2: 15, 3: 12, 4: 12, 5: 12, 6: 15, 7: 15}


class TestSetFinder(TestCase):
    def test_get_cards_from_board(self):
        my_cards = []
        for i in range(7):
            image = BoardRecognition(
                img=os.path.join(path, f"set_board{i}.jpg")
            )
            my_cards = image.extract_cards_from_board()
            with open(f"set_board_cards_{i}.p", "wb") as f:
                pickle.dump(my_cards, f)
        self.assertEqual(len(my_cards), board_cards.get(i))
