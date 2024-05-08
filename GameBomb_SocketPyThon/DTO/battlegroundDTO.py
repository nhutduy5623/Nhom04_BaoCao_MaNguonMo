import pygame
from player import Player
from bomb import Bomb

class BattleGroundDTO():
    def __init__(self, groundMatrix, player, player2):
        self.groundMatrix = groundMatrix
        self.player = player
        self.player2 = player2        

   # Getter cho groundMatrix
    def get_groundMatrix(self):
        return self.groundMatrix

    # Setter cho groundMatrix
    def set_groundMatrix(self, value):
        self.groundMatrix = value

    # Getter cho player
    def get_player(self):
        return self.player

    # Setter cho player
    def set_player(self, value):
        self.player = value

    # Getter cho player2
    def get_player2(self):
        return self.player2

    # Setter cho player2
    def set_player2(self, value):
        self.player2 = value

