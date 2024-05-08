import pygame
from asyncio.windows_utils import pipe
from distutils.spawn import spawn
from json import load
from tkinter import CENTER
import sys, random

class PlayerDTO():
    def __init__(self, flag_StartGame, centerx, centery, status, vel, playerIndex, recoverTime, listBomb):
        self.flag_StartGame = flag_StartGame
        self.centerx = centerx
        self.centery = centery
        self.vel = vel
        self.playerIndex = playerIndex
        self.maxBomb = 2
        self.status = status
        self.recoverTime = recoverTime
        self.listBomb = listBomb
        
      # Getter cho centerx
    def get_centerx(self):
        return self.centerx

    # Setter cho centerx
    def set_centerx(self, value):
        self.centerx = value

    # Getter cho centery
    def get_centery(self):
        return self.centery

    # Setter cho centery
    def set_centery(self, value):
        self.centery = value

    # Getter cho status
    def get_status(self):
        return self.status

    # Setter cho status
    def set_status(self, value):
        self.status = value

    # Getter cho vel
    def get_vel(self):
        return self.vel

    # Setter cho vel
    def set_vel(self, value):
        self.vel = value

    # Getter cho playerIndex
    def get_playerIndex(self):
        return self.playerIndex

    # Setter cho playerIndex
    def set_playerIndex(self, value):
        self.playerIndex = value

    # Getter cho maxBomb
    def get_maxBomb(self):
        return self.maxBomb

    # Setter cho maxBomb
    def set_maxBomb(self, value):
        self.maxBomb = value

    # Getter cho recoverTime
    def get_recoverTime(self):
        return self.recoverTime

    # Setter cho recoverTime
    def set_recoverTime(self, value):
        self.recoverTime = value

    def get_ListBomb(self):
        return self.listBomb

    def set_ListBomb(self, value): 
        self.listBomb = value

        


        
            