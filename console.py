from main import *
import sys

board = PyramidBoard()
deck = board.deck
deck.shuffle_deck()


def validate_input(text):
    while True:
        try:
            command = int(input(text))
        except ValueError:
            print('Whoops! Wrong value!')
        else:
            return command

def render_board():
    print(len(board.board_cards))
    print(len(deck.cards))


def initialize_board():
    spaces = 70

    iterator = iter(deck)
    for i in range(7):
        print(' ' * spaces, end='')
        for j in range(i+1):
            position = 1
            element = next(iterator)

            board.add_board_card(element.id)
            element.position = position
            deck.remove_card(element.id)

            position += 1

            if i != 6:
                print('[ hidden card ]', end='  ')
                element.blockers = [position + i + 1, position + j + 2]
            else:
                print(('[ "id:{}" {} ]').format(element.id, element.name), end='  ')



        print(' ', end='\n')
        print(' ', end='\n')
        spaces -= 7

    print('Deck: ', end=' ')
    for x in deck:
        print(('[ "id:{}" {} ]').format(x.id, x.name), end='  |  ')
    print(' ', end='\n')


def initialize_game():
    while True:
        command = validate_input('enter "1" to add cards, "0" for exit: ')

        if command == 0:
            sys.exit()

        first_card = validate_input('enter first card id: ')
        second_card = validate_input('enter second card id: ')

        cards_id = board.add_cards(first_card, second_card)

        render_board()

initialize_board()
initialize_game()
