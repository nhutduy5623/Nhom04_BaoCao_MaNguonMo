import pygame
from bombBang import BombBang

class Bomb():
    def __init__(self, rect, surfaceList):
        self.rect = rect
        self.surfaceList = surfaceList
        self.surfaceIndex = 0
        self.surface = surfaceList[self.surfaceIndex]
        self.status = 0
        self.timer = 0
        self.bombBangSize = 1     
        self.bombBang_Surface = []
        self.setUpSurfaceBombBang()
        self.bombBang = [BombBang(self.bombBang_Surface[0][self.bombBangSize-1]),BombBang(self.bombBang_Surface[1][self.bombBangSize-1]),BombBang(self.bombBang_Surface[2][self.bombBangSize-1]),BombBang(self.bombBang_Surface[3][self.bombBangSize-1])]
        self.bombBangNone = BombBang(self.bombBang_Surface[0][self.bombBangSize-1])

    def animate(self):
        if self.surfaceIndex == 0:
            self.rect.centery -=3
            self.surfaceIndex = 1
        else:
            self.rect.centery +=3
            self.surfaceIndex = 0
        self.surface = self.surfaceList[self.surfaceIndex]

    def draw(self, screen):
        screen.blit(self.surface, self.rect)
    
    def drawBombBang(self, screen):
        for BombBang in self.bombBang:
            BombBang.drawBombBang(screen)

    def placeABomb(seft, playerRect):
        seft.status = 1
        seft.rect = playerRect

    def setSurface_Rect(self, playerRect, indexSurface):
        self.rect = playerRect
        self.surface = self.surfaceList[indexSurface]

    def setStatus(self, status):
        self.status = status
        if status == 1:
            self.timer=0

    def getStatus(self):
        return self.status
    
    def setRect(self, rect):
        self.rect = rect

    def getRect(self):
        return self.rect
    
    def setRectWithPosition(self, bombRectx, bombRecty):
        self.rect = self.surface.get_rect(center=(bombRectx, bombRecty))

    def increaseTimer(self, value):
        self.timer+=value
    
    def getTimer(self):
        return self.timer
    
    def getBombBang(self):
        return self.bombBang
    
    def getBombSize(self):
        return self.bombBangSize
    
    def Bang(self):
        self.status = 2
        i=0
        for bang in self.bombBang:
            if i==0:
                bang.setRectCenterX_Y(self.getRect().centerx,self.getRect().centery-25*self.bombBangSize)
            elif i==1:
                bang.setRectCenterX_Y(self.getRect().centerx,self.getRect().centery+25*self.bombBangSize)
            elif i==2:
                bang.setRectCenterX_Y(self.getRect().centerx-25*self.bombBangSize,self.getRect().centery)
            elif i==3:
                bang.setRectCenterX_Y(self.getRect().centerx+25*self.bombBangSize,self.getRect().centery)
            i+=1
        
    
    def hide(self):
        self.rect = self.surface.get_rect(center=(-1000, 200))
        self.bombBang = [BombBang(self.bombBang_Surface[0][self.bombBangSize-1]),BombBang(self.bombBang_Surface[1][self.bombBangSize-1]),BombBang(self.bombBang_Surface[2][self.bombBangSize-1]),BombBang(self.bombBang_Surface[3][self.bombBangSize-1])]
        self.Bang()        
        self.status = 0
        

    def setUpSurfaceBombBang(self):
        for i in range(1, 6):
            arrayTemp = []
            if i==1:
                direction = 'up'
            if i==2:
                direction = 'down'
            if i==3:
                direction = 'left'
            if i==4:
                direction = 'right'        
            for j in range(1, 11):
                skin = pygame.image.load('./img/Bomb/bombbang_'+str(direction)+''+str(j)+'.png')
                if i==1 or i==2:
                    arrayTemp.append(pygame.transform.scale(skin, (45,45*(j+1))))
                else:
                    arrayTemp.append(pygame.transform.scale(skin, (45*(j+1),45)))
            skin = pygame.image.load('./img/Bomb/bombbang_'+str(direction)+''+str(1)+'.png')
            if i==1 or i==2:
                arrayTemp.append(pygame.transform.scale(skin, (45,1)))
            else:
                arrayTemp.append(pygame.transform.scale(skin, (1,45)))
            self.bombBang_Surface.append(arrayTemp)
        