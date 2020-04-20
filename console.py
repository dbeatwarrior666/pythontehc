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

    if len(board.board_cards) == 0:
        print('*' * 70)
        print('*' * 70)
        print('*' * 70)
        print('*' * 22, end='WOW INCREDIBLE YOU WIN!')
        print('*' * 25)
        print('*' * 70)
        print('*' * 70)
        print('*' * 70)

    spaces = 70
    position = 1
    for i in range(7):
        print(' ' * spaces, end='')
        for j in range(i + 1):
            element = board.get_card_by_position(position)
            position += 1

            if element is None:
                print(' ' * 12, end='      ')
                continue
            if hasattr(element, 'blockers') and len(element.blockers) > 0:
                print('[ hidden card ] ', end=' ')

            else:
                print('[ "id:{}" {} ]'.format(element.id, element.name), end='  ')

        print(' ', end='\n')
        print(' ', end='\n')
        spaces -= 7

    print('Deck: ', end=' ')
    for x in deck:
        print('[ "id:{}" {} ]'.format(x.id, x.name), end='  |  ')
    print(' ', end='\n')


def initialize_board():
    spaces = 70

    iterator = iter(deck)
    position = 1
    for i in range(7):
        print(' ' * spaces, end='')
        for j in range(i + 1):

            element = next(iterator)

            board.add_board_card(element.id)
            element.position = position
            deck.remove_card(element.id)



            if i != 6:
                element.blockers = [position + i + 1, position + i + 2]
                print('[ hidden card ] ', end=' ')
            else:
                print('[ "id:{}" {} ]'.format(element.id, element.name), end='   ')

            position += 1

        print(' ', end='\n')
        print(' ', end='\n')
        spaces -= 7

    print('Deck: ', end=' ')
    for x in deck:
        print('[ "id:{}" {} ]'.format(x.id, x.name), end='  |  ')
    print(' ', end='\n')


def initialize_game():
    while True:
        command = validate_input('enter "1" to add cards, "0" for exit: ')

        if command == 0:
            sys.exit()

        while True:
            try:
                first_card_id = validate_input('enter first card id: ')
                second_card_id = validate_input('enter second card id: ')

                board.add_cards(first_card_id, second_card_id)
            except RuntimeError:
                print('You cant add this card! Try again!')
            else:
                break

        render_board()


initialize_board()
initialize_game()
