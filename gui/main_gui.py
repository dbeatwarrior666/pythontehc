from PySide import QtGui
import sys
from gui import Ui_Form
from main import *
from functools import partial

# Create app
import sys

app = QtGui.QApplication(sys.argv)
Form = QtGui.QWidget()
ui = Ui_Form()
ui.setupUi(Form)
Form.show()

board = PyramidBoard()
deck = board.deck
deck.shuffle_deck()

# Code here

def initialize_board():
    # showing start button
    buttons = vars(ui)
    for button in buttons:
        buttons[button].hide()

        if 'card' in str(button):
            try:
                buttons[button].id = int(button.split('_')[1])
            except ValueError:
                continue

    ui.graphicsView.show()
    ui.start_game_button.show()

    # window + bg configure
    ui.graphicsView.lower()
    Form.setFixedSize(Form.size())

    # setting styles
    stylesheet = """
        QGraphicsView{
            background-image: url(background.jpg);
        }
        QPushButton {
            border-radius: 10px;
            border: 1px solid #000;
            background-color: white;
            background-image: url(cards/t-shirt.png);
        }

        QPushButton:hover {
            border: 4px solid #476D98;
        }

        QPushButton#start_game_button{
            background: none;
            background-color: #476D98;
            border: 2px solid #476D98;
            color: #fff;
            font-size: 25pt;
            font-family: Comic Sans MS;
            max-width: 300px;
            max-height: 100px;
            margin-left: 140px;
            margin-top: 50px;
        }
        QPushButton:hover#start_game_button{
            background-color: #7194BD;
        }
        
        QPushButton[selected = 'true'] {
            border: 3px solid red;
        }
    """
    app.setStyleSheet(stylesheet)

    render_board()
    initialize_events()


def render_board():
    position = 1
    iterator = iter(deck)
    for line in range(7):
        for card_position in range(line + 1):
            element = next(iterator)

            board.add_board_card(element)
            element.position = position
            deck.remove(element)

            if line != 6:
                element.blockers = [position + line + 1, position + line + 2]
            else:
                show_card(element)

            position += 1

    start_top_deck_card = next(iter(deck))
    show_top_deck_card(start_top_deck_card)
    start_top_deck_card.is_top_deck = True


def get_card_button_by_card(card):
    button_cards = vars(ui)

    if not hasattr(card, 'position'):
        return ui.deck_top_card

    for button_card in button_cards:
        if hasattr(button_cards[button_card], 'id') and button_cards[button_card].id == card.position:
            return button_cards[button_card]


def get_card_by_card_button(card_button):
    if hasattr(card_button, 'id'):
        return board.get_card_by_position(card_button.id)
    return deck.get_top_deck_card()


def make_selected(card_button):
    card = get_card_by_card_button(card_button)
    board.selected_card = card

    # styles
    card_button.setProperty('selected', 'true')
    card_button.style().unpolish(card_button)
    card_button.style().polish(card_button)
    card_button.update()


def make_deselected(card_button):
    delattr(board, 'selected_card')

    # styles
    card_button.setProperty('selected', 'false')
    card_button.style().unpolish(card_button)
    card_button.style().polish(card_button)
    card_button.update()


def show_top_deck_card(card):
    top_deck_card_button = ui.deck_top_card
    top_deck_card_button.setStyleSheet('background-image: url(' + card.background_url + ')')


def show_card(card):
    card_button = get_card_button_by_card(card)
    card_button.setStyleSheet('background: none')
    card_button.setStyleSheet('background-image: url(' + card.background_url + ')')


def initialize_events():
    ui.start_game_button.clicked.connect(start_game_clicked)
    board.iter_deck = iter(deck)
    ui.deck.clicked.connect(deck_clicked)
    button_cards = vars(ui)

    for button_card in button_cards:
        if 'card' in button_card.split('_'):
            button_cards[button_card].clicked.connect(partial(card_clicked, button_cards[button_card]))


def start_game_clicked():

    buttons = vars(ui)
    for button in buttons:
        buttons[button].show()
    ui.start_game_button.hide()


def update_board():
    for card in board.board_cards:
        if len(card.blockers) == 0:
            show_card(card)


def delete_card_from_board(card):
    card_button = get_card_button_by_card(card)
    card_button.hide()
    if card.position == 1:
        ui.deck_top_card.hide()
        ui.deck.hide()
        ui.start_game_button.show()
        ui.start_game_button.setText('YOU WIN')


def deck_clicked():
    try:
        iter_deck = board.iter_deck
        new_card = next(iter(iter_deck))
    except StopIteration:
        board.iter_deck = iter(deck)

        iter_deck = board.iter_deck
        new_card = next(iter(iter_deck))

    show_top_deck_card(new_card)
    top_deck_card = deck.get_top_deck_card()
    delattr(top_deck_card, 'is_top_deck')
    new_card.is_top_deck = True


def card_clicked(self):
    if hasattr(board, 'selected_card'):
        first_card = board.selected_card
        second_card = get_card_by_card_button(self)

        result = board.add_two_cards(first_card.id, second_card.id)

        if result[0] is True:
            board.delete_card(first_card)
            if first_card.is_top_deck:
                delattr(first_card, 'is_top_deck')
                new_card = next(iter(deck))
                show_top_deck_card(new_card)
                new_card.is_top_deck = True
            else:
                delete_card_from_board(first_card)
        if result[1] is True:
            if second_card.is_top_deck:
                delattr(second_card, 'is_top_deck')
                new_card = next(iter(deck))
                show_top_deck_card(new_card)
                new_card.is_top_deck = True
            else:
                delete_card_from_board(second_card)

        update_board()
        make_deselected(get_card_button_by_card(first_card))
    else:
        make_selected(self)


initialize_board()
# Run main loop
sys.exit(app.exec_())
