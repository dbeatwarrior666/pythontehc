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
        self.background_url = "cards/"+self.suit+"/"+self.name+'.png'
        self.is_top_deck = False

        Card.cardId += 1


class Deck:
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['Spades', 'Clubs', 'Hearts', 'Diamonds']

    def __init__(self):
        self.cards = []

        for x in self.suits:
            for y in range(len(self.values)):
                card = Card(x, y+1, self.values[y-1])
                self.cards.append(card)

    def __iter__(self):
        return MyIterator(self.cards)

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Deck, cls).__new__(cls)
        return cls.instance

    def shuffle_deck(self):
        shuffle(self.cards)

    def remove(self, card):
        self.cards.remove(card)

    def get_top_deck_card(self):
        for card in self.cards:
            if hasattr(card, 'is_top_deck'):
                return card


class PyramidBoard:
    def __init__(self):
        self.board_cards = []
        self.deck = Deck()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PyramidBoard, cls).__new__(cls)
        return cls.instance

    def __iter__(self):
        return MyIterator(self.board_cards)

    @staticmethod
    def has_blockers(card):
        if len(card.blockers) != 0:
            return True
        return False

    def add_board_card(self, card):
        self.board_cards.append(card)

    def add_two_cards(self, first_id, second_id):

        first_id_card = self.get_card_by_id(first_id)
        second_id_card = self.get_card_by_id(second_id)

        return_array = [False, False]

        if self.has_blockers(first_id_card) or self.has_blockers(second_id_card):
            return return_array

        if first_id_card in self.deck and second_id_card in self.deck:
            return return_array

        if first_id_card.value != 13 and second_id_card.value != 13:
            if first_id_card.value + second_id_card.value == 13:
                self.update_blockers(first_id_card)
                self.update_blockers(second_id_card)
                self.delete_card(first_id_card)
                self.delete_card(second_id_card)
                return_array = [True, True]

        if first_id_card.value == 13:
            self.update_blockers(first_id_card)
            self.delete_card(first_id_card)
            return_array[0] = True

        if second_id_card.value == 13:
            self.update_blockers(second_id_card)
            self.delete_card(second_id_card)
            return_array[1] = True

        return return_array

    def delete_card(self, card):
        if card in self.board_cards:
            self.board_cards.remove(card)
        elif card in self.deck:
            self.deck.remove(card)

    def get_card_by_id(self, card_id):
        for card in self.board_cards:
            if card.id == card_id:
                return card

        for card in self.deck:
            if card.id == card_id:
                return card

    def get_card_by_position(self, card_position):
        for card in self.board_cards:
            if card.position == card_position:
                return card

    def update_blockers(self, card):
        for card_elem in self.board_cards:
            if hasattr(card, 'position') and card.position in card_elem.blockers:
                card_elem.blockers.remove(card.position)
