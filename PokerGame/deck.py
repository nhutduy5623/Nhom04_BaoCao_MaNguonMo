import random
from card import Card

class Deck:
    def __init__(self):
        self.cards = []
        self.generate_deck()

    def generate_deck(self):
        suits = ['Hearts', 'Tiles', 'Clovers', 'Pikes']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'A']
        for suit in suits:
            for rank in ranks:
                if rank.isdigit():
                    value = int(rank)
                elif rank in ['Jack', 'Queen', 'King']:
                    value = 10 + ranks.index(rank) - ranks.index('Jack') + 1  # Jack=11, Queen=12, King=13
                else:
                    value = 14  # Ace
                name = f"{rank}"
                card = Card(name, value, suit)
                self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            print("Deck is empty!")
