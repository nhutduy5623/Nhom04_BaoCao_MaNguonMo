class BombDTO():
    def __init__(self, centerx, centery, status, timer, bombBangSize):
        self.centerx = centerx
        self.centery = centery
        self.status = status
        self.timer = timer
        self.bombBangSize = bombBangSize   
    
    def get_centerx(self):
        return self.centerx
        
    def set_centerx(self, value):
        self.centerx = value
        
    def get_status(self):
        return self.status
        
    def set_status(self, value):
        self.status = value
        
    def get_timer(self):
        return self.timer
        
    def set_timer(self, value):
        self.timer = value
        
    def get_bombBangSize(self):
        return self.bombBangSize
        
    def set_bombBangSize(self, value):
        self.bombBangSize = value
