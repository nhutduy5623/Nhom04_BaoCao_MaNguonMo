import pygame
class Card:
    def __init__(self, name, value,suit):
        self.name = name
        self.value = value
        self.suit = suit

    def __str__(self):
        return f"{self.suit}_{self.name}_white"
