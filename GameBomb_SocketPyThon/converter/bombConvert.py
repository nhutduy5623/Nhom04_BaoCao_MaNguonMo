import pygame
from DTO.bombDTO import BombDTO
from bomb import Bomb

class bombConvert():
    def toDTO(self, bomb):        
        return BombDTO(bomb.rect.centerx, bomb.rect.centery, bomb.status, bomb.timer, bomb.bombBangSize)
    def toBomb(self, bombDTO):
        bombSkin = pygame.image.load('./img/bomb.gif')
        bombSurface1 = pygame.transform.scale(bombSkin, (50,50))
        bombSurface2 = pygame.transform.scale(bombSkin, (50,53))
        bombSurfaceList = [bombSurface1, bombSurface2]
        bombIndex = 0
        bombSurface = bombSurfaceList[bombIndex]
        bombRect = bombSurface.get_rect(center=(-1000, 100))
        bombRect.centerx = bombDTO.centerx
        bombRect.centery = bombDTO.centery
        bomb = Bomb(bombRect, bombSurfaceList)
        bomb.status = bombDTO.status
        bomb.timer = bombDTO.timer
        bomb.bombBangSize = bombDTO.get_bombBangSize()   
        return bomb