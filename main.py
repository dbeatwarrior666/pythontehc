import types
from random import shuffle


class MyIterator:
    def __init__(self, cards):
        self.cards = cards.copy()
        self.value = 0
        self.end = len(cards)

    def __iter__(self):
        return self

    def __next__(self):
        if self.value >= self.end:
            raise StopIteration
        current = self.cards[self.value]
        self.value += 1

        return current


class Card:

    cardId = 0

    def __init__(self, suit, value, name):
        self.suit = suit
        self.name = name
        self.value = value
        self.id = Card.cardId

        Card.cardId += 1


class Deck:
    values = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
    suits = ['Spades', 'Hearts', 'Clubs', 'Diamonds']

    def __init__(self):
        self.cards = []

        for x in self.suits:
            for y in range(len(self.values)):
                card = Card(x, y+1, self.values[y])
                self.cards.append(card)

    def __iter__(self):
        return MyIterator(self.cards)

    def shuffle_deck(self):
        shuffle(self.cards)

    def remove_card(self, card_id):
        for x in self.cards:
            if x.id == card_id:
                self.cards.remove(x)

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Deck, cls).__new__(cls)
        return cls.instance


class PyramidBoard:
    def __init__(self, func=None):
        self.board_cards = []
        if func is None:
            self.deck = Deck()
        else:
            self.execute = types.MethodType(func, self)

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PyramidBoard, cls).__new__(cls)
        return cls.instance

    def execute_for_gui(self):
        # code here
        pass

    def add_board_card(self, card_id):
        for x in self.deck:
            if x.id == card_id:
                self.board_cards.append(x)

    def add_cards(self, first_id, second_id):
        first_id_card = 0
        second_id_card = 0

        for x in self.board_cards:
            if x.id == first_id:
                first_id_card = x
            if x.id == second_id:
                second_id_card = x

        for y in self.deck:
            if y.id == first_id:
                first_id_card = y
            if y.id == second_id:
                second_id_card = y

        if first_id_card.value != 13 and second_id_card.value != 13:
            if first_id_card.value + second_id_card.value == 13:
                self.delete_card(first_id_card)
                self.delete_card(second_id_card)
                return [first_id, second_id]
        if first_id_card.value == 13:
            self.delete_card(first_id_card)
            return [first_id]

        self.delete_card(second_id_card)
        return [second_id]

    def delete_card(self, card_id):
        card_deleted = False

        for x in self.board_cards:
            if x.id == card_id:
                self.board_cards.remove(x)
                card_deleted = True

        if not card_deleted:
            for x in self.deck:
                if x.id == card_id:
                    self.deck.remove_card(x)
