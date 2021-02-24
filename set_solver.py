import os

from setsolver.board import Board
from setsolver.image_detection.board_recognition import BoardRecognition
from setsolver.image_detection.card_recognition import CardRecognition
from setsolver.set_finder import find_all_sets

input_image_dir = path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "setsolver",
    "image_detection",
    "board_input",
)
input_image_name = "set_board2.jpg"

if __name__ == "__main__":
    abstract_cards = set()
    board_img = BoardRecognition(
        os.path.join(input_image_dir, input_image_name)
    )
    set_cards = board_img.extract_cards_from_board()
    for extracted_card in set_cards:
        card = CardRecognition(extracted_card)
        card.process_all_properties()
        if card.abstract_card is not None:
            abstract_cards.add(card.abstract_card)

    sets = find_all_sets(Board(abstract_cards))
    print(sets)
