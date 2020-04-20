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
        self.blockers = []

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

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Deck, cls).__new__(cls)
        return cls.instance

    def shuffle_deck(self):
        shuffle(self.cards)

    def remove_card(self, card_id):
        for x in self.cards:
            if x.id == card_id:
                self.cards.remove(x)


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

    def __iter__(self):
        return MyIterator(self.board_cards)

    @staticmethod
    def has_blockers(card_obj):
        if len(card_obj.blockers) != 0:
            return True
        return False

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

        if self.has_blockers(first_id_card) or self.has_blockers(second_id_card):
            raise RuntimeError()

        if first_id_card in self.deck and second_id_card in self.deck:
            raise RuntimeError()

        if first_id_card.value != 13 and second_id_card.value != 13:
            if first_id_card.value + second_id_card.value == 13:
                self.update_blockers(first_id)
                self.update_blockers(second_id)
                self.delete_card(first_id)
                self.delete_card(second_id)

        if first_id_card.value == 13:
            self.update_blockers(first_id)
            self.delete_card(first_id)

        if second_id_card.value == 13:
            self.update_blockers(second_id)
            self.delete_card(second_id)

        return True

    def delete_card(self, card_id):
        card_deleted = False

        for x in self.board_cards:
            if x.id == card_id:
                self.board_cards.remove(x)
                card_deleted = True

        if not card_deleted:
            self.deck.remove_card(card_id)

    def get_card_by_id(self, card_id):
        for x in self.board_cards:
            if x.id == card_id:
                return x

        for y in self.deck:
            if y.id == card_id:
                return y

    def get_card_by_position(self, card_position):
        for card in self.board_cards:
            if card.position == card_position:
                return card

    def update_blockers(self, card_id):
        card = self.get_card_by_id(card_id)

        for card_elem in self.board_cards:
            if hasattr(card, 'position') and card.position in card_elem.blockers:
                card_elem.blockers.remove(card.position)
