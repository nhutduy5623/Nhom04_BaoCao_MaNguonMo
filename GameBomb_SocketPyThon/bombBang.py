import pygame
class BombBang():
    def __init__(self, surfaceBombBang):
        self.rect = 1000
        self.surfaceBombBang = surfaceBombBang
        self.bombExplodeSize = 1

    def drawBombBang(self, screen):
        screen.blit(self.surfaceBombBang, self.rect)

    def setRectCenterx(self, value):
        self.rect.centerx=value
    
    def setRectCentery(self, value):
        self.rect.centery=value

    def setRectCenterX_Y(self, centerx, centery):
        self.rect = self.surfaceBombBang.get_rect(center=(centerx, centery))

    def setRect(self, rect):
        self.rect = rect

    def getRect(self):
        return self.rect
    
    def hide(self):
        self.rect = self.surfaceBombBang.get_rect(center=(-1000, 0))
    
    def areCollidingPlayer(self, obj):
        if self.rect.colliderect(obj):
            return True
        return False      

    def setSurfaceBombbang(self, surfacce):
        self.surfaceBombBang = surfacce

    # def setUpSurfaceExplore(self):
    #     for i in range(1, 5):
    #         arrayTemp = []
    #         if i==1:
    #             direction = 'up'
    #         if i==2:
    #             direction = 'down'
    #         if i==3:
    #             direction = 'left'
    #         if i==4:
    #             direction = 'right'
    #         for j in range(1, 11):
    #             skin = pygame.image.load('./img/Bomb/bombbang_'+direction+''+j+'.png')
    #             if i==1 or i==2:
    #                 arrayTemp.append(pygame.transform.scale(skin, (50,50*j)))
    #             else:
    #                 arrayTemp.append(pygame.transform.scale(skin, (50*j,50)))
    #         self.Explode_Surface.append(arrayTemp)
        