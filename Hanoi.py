import random as rand, pygame as py
from pygame.locals import *

py.init()
py.mixer.quit()
    
class Disco(py.sprite.Sprite):
    def __init__(self, w, h, x, y):
        py.sprite.Sprite.__init__(self)
        self.image = py.Surface([w, h])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = [rand.randint(0, 255), rand.randint(0, 255), rand.randint(0, 255)]
        
    def draw(self, screen):
        py.draw.rect(screen, self.color, self.rect)
        
class Game:
    def __init__(self):
        self.w = 1280
        self.h = 720
        self.window = py.display.set_mode((self.w, self.h))
        self.isRunning = True
        self.n = 10
        self.width = 200
        self.height = 40
        self.centerx0 = 200
        self.centerx1 = self.centerx0 + 400
        self.centerx2 = self.centerx1 + 400
        self.centery = 500
        self.discos = []
        self.discos1 = []
        self.discos2 = []
        self.torre0 = Disco(40, 320, self.centerx0 - 20, self.centery - 300)
        self.torre1 = Disco(40, 320, self.centerx1 - 20, self.centery - 300)
        self.torre2 = Disco(40, 320, self.centerx2 - 20, self.centery - 300)
        self.black = (0, 0, 0)
        self.torre0.color = self.torre1.color = self.torre2.color = self.black
        py.display.set_caption("Torres de Hanoi")
        for i in range(self.n):
            self.discos.append(Disco(self.width-i*20, self.height, self.centerx0 - (self.width-i*20)/2, self.centery - self.height/2 - i*self.height))
        self.discos0 = self.discos    
        self.clock = py.time.Clock()
        self.clock.tick(15)
        self.hanoi(self.n, 0, 2, 1)
    
    def draw(self):
        self.window.fill((255, 255, 255))
        self.torre0.draw(self.window)
        self.torre1.draw(self.window)
        self.torre2.draw(self.window)
        for disco in set(self.discos0 + self.discos1 + self.discos2):
            disco.draw(self.window)
        py.display.flip()
    
    def hanoi(self, n, origen, destino, aux):
        if n > 0:
            self.hanoi(n - 1, origen, aux, destino)
            self.moverATorre(origen, destino)
            self.draw()
            self.hanoi(n - 1, aux, destino, origen)
    
    def gameLoop(self):
        while self.isRunning:
            self.events()
            self.draw()
            self.clock.tick(60)
            
    def events(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                self.isRunning = False
    
    def moverATorre(self, torre_origen, torre_destino):
        if torre_origen == 0:
            disco = self.discos0.pop()
            if torre_destino == 1:
                disco.rect.x = self.centerx1 - disco.rect.width/2
                disco.rect.y = self.centery - self.height/2 - len(self.discos1)*self.height
                self.discos1.append(disco)
            elif torre_destino  == 2:
                disco.rect.x = self.centerx2 - disco.rect.width/2
                disco.rect.y = self.centery - self.height/2 - len(self.discos2)*self.height
                self.discos2.append(disco)
        elif torre_origen == 1:
            disco = self.discos1.pop()
            if torre_destino == 0:
                disco.rect.x = self.centerx0 - disco.rect.width/2
                disco.rect.y = self.centery - self.height/2 - len(self.discos0)*self.height
                self.discos0.append(disco)
            elif torre_destino == 2:
                disco.rect.x = self.centerx2 - disco.rect.width/2
                disco.rect.y = self.centery - self.height/2 - len(self.discos2)*self.height
                self.discos2.append(disco)
        elif torre_origen == 2:
            disco = self.discos2.pop()
            if torre_destino == 0:
                disco.rect.x = self.centerx0 - disco.rect.width/2
                disco.rect.y = self.centery - self.height/2 - len(self.discos0)*self.height
                self.discos0.append(disco)
            elif torre_destino  == 1:
                disco.rect.x = self.centerx1 - disco.rect.width/2
                disco.rect.y = self.centery - self.height/2 - len(self.discos1)*self.height
                self.discos1.append(disco)
            

if __name__ == '__main__':
    game = Game()
    game.gameLoop()
    py.quit()
