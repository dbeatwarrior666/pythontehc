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


def end_game():
    print('*' * 70, '*' * 70, '*' * 70, sep='\n', end='\n')
    print('*' * 22, '*' * 25, sep='WOW INCREDIBLE YOU WIN!', end='\n')
    print('*' * 70, '*' * 70, '*' * 70, sep='\n', end='\n')


def render_board():

    if len(board.board_cards) == 0:
        end_game()
        return

    spaces = 70
    position = 1
    for counter in range(7):
        print(' ' * spaces, end='')
        for second_counter in range(counter + 1):
            element = board.get_card_by_position(position)
            position += 1

            if element is None:
                print(' ' * 12, end='      ')
                continue

            if hasattr(element, 'blockers') and len(element.blockers) > 0:
                print('[ hidden card ] ', end=' ')

            else:
                print('[ "id:{}" {} ]'.format(element.id, element.name), end='   ')

        print(' ', sep='\n', end='\n')
        spaces -= 7

    print(' ', sep='\n', end='\n')
    print('Deck: ', end=' ')
    for x in deck:
        print('[ "id:{}" {} ]'.format(x.id, x.name), end='  |  ')
    print(' ', end='\n')


def initialize_board():
    spaces = 70

    iterator = iter(deck)
    position = 1

    for line in range(7):
        print(' ' * spaces, end='')
        for card_position in range(line + 1):
            element = next(iterator)

            board.add_board_card(element)
            element.position = position
            deck.remove(element)

            if line != 6:
                element.blockers = [position + line + 1, position + line + 2]
                print('[ hidden card ] ', end=' ')
            else:
                print('[ "id:{}" {} ]'.format(element.id, element.name), end='   ')

            position += 1

        print(' ', sep='\n', end='\n')
        spaces -= 7

    print(' ', sep='\n', end='\n')
    print('Deck: ', end=' ')
    for x in deck:
        print('[ "id:{}" {} ]'.format(x.id, x.name), end='  |  ')
    print(' ', end='\n')

    initialize_game()


def initialize_game():
    while True:
        command = validate_input('enter "1" to add cards, "0" for exit: ')

        if command == 0:
            sys.exit()

        while True:
            try:
                first_card_id = validate_input('enter first card id: ')
                second_card_id = validate_input('enter second card id: ')

                board.add_two_cards(first_card_id, second_card_id)
            except RuntimeError:
                print('You cant add this card! Try again!')
            else:
                break

        render_board()


initialize_board()

