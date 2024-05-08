import pygame
from asyncio.windows_utils import pipe
from distutils.spawn import spawn
from json import load
from multiprocessing.connection import wait
from tkinter import CENTER
import pygame, sys, random
from bomb import Bomb
from converter.bombConvert import bombConvert

class Player():

    def __init__(self, rect, surfaceList, bomb):
        self.startRect = [rect.centerx,rect.centery]
        self.rect = rect
        self.vel = 4
        self.surfaceList = surfaceList
        self.surface = surfaceList[0]
        self.maxBomb = 1
        self.listBomb = bomb
        self.status = 1
        self.recoverTime = 0
        self.flag_StartGame = 0

    def draw(self, screen):
        screen.blit(self.surface, self.rect)

    def update(seft, playerRect):
        seft.rect = playerRect

    def setSurface_Rect(self, playerRect, indexSurface):
        self.rect = playerRect
        self.surface = self.surfaceList[indexSurface]
        

    def move(self, direction):
        if self.status == 1:
            if direction == "left":
                if self.ValidNextStep("left"):
                    self.rect.centerx -= self.vel
            if direction == "right":
                if self.ValidNextStep("right"):
                    self.rect.centerx += self.vel
            if direction == "up":
                if self.ValidNextStep("up"):
                    self.rect.centery -= self.vel
            if direction == "down":
                if self.ValidNextStep("down"):
                    self.rect.centery += self.vel

    def ValidNextStep(self, direction):
        if direction == "left":
            if self.rect.centerx - self.vel <= 50:
                return False
        if direction == "right":
            if self.rect.centerx + self.vel >= 800-50:
                return False
        if direction == "up":
            if self.rect.centery - self.vel <= 0+50:
                return False
        if direction == "down":
            if self.rect.centery + self.vel >= 800-50:
                return False
        return True
    
    def checkTouchingObj(self, Obj):
        if Obj == 0:
            return False
        if self.rect.colliderect(Obj):
            return True
        return False

    def getRect(self):
        return self.rect
    
    def getSurface(self):
        return self.surface
    
    def placeABomb(self, bombRectx, bombRecty, sound_PlaceBomb):
        for i in range(len(self.listBomb)):
            if self.listBomb[i].getStatus() == 0:
                self.listBomb[i].setStatus(1)
                self.listBomb[i].setRectWithPosition(bombRectx,bombRecty)
                sound_PlaceBomb.play()
                break
    
    def getListBomb(self):
        return self.listBomb
    
    def increaseTimer_BombBang(self, value, sound_BombBang):
        for bomb in self.listBomb:
            if bomb.getStatus()==1 or bomb.getStatus()==2:
                bomb.increaseTimer(value)
                if bomb.getTimer() == 2000:
                    bomb.Bang()
                    sound_BombBang.play()
                if bomb.getTimer() == 2500:
                    bomb.hide()

    def gameOver(self):
        self.status = 0
        self.surface = self.surfaceList[1]

    def gameWaiting(self):
        self.status = 2
        self.surface = self.surfaceList[1]

    def recover(self):
        self.surface = self.surfaceList[0]
        self.rect.centerx = self.startRect[0]
        self.rect.centery = self.startRect[1]       
        self.status = 1

    def isGameOver(self):
        if self.status == 0:
            return True
        return False

    def getCenterx(self):
        return self.rect.centerx

    def getCentery(self):
        return self.rect.centery

    def getVel(self):
        return self.vel
    
    def getMaxBomb(self):
        return self.maxBomb
    
    def getStatus(self):
        return self.status
    
    def getRecoverTime(self):
        return self.recoverTime
        
    def setByDTO(self, playerDTO):
        self.rect.centerx = playerDTO.get_centerx()
        self.rect.centery = playerDTO.get_centery()
        self.status = playerDTO.get_status()
        self.vel = playerDTO.get_vel()
        self.maxBomb = playerDTO.get_maxBomb()
        self.recoverTime = playerDTO.get_recoverTime()
        self.listBomb = []
        for bombDTO in playerDTO.get_ListBomb():
            self.listBomb.append(bombConvert().toBomb(bombDTO))


        
            
            