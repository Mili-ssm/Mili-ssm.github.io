from dataclasses import dataclass, field
import random
import numpy as np
from tqdm import tqdm
import pygame


BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
WHITE1 = (0, 0, 200)
WHITE2 = (0, 200, 0)
WINDOW_HEIGHT = 1000
WINDOW_WIDTH = 1000

@dataclass(slots=True)
class Celula():
    _x : int
    _y : int

    vida : int = field(default_factory=lambda: random.randint(-25, 0))

    def __call__(self, mundo):
        for x in range(-1,1):
            for y in range(-1,1):
                if mundo[self._x + x][self._y + y].vida/20 < -1:
                    self.vida -= 1
        return (min(255,int(255 * abs(self.vida)/400)),0,0)
        
@dataclass(slots=True)
class CelulaViva(Celula):

    def __call__(self, mundo:'Mundo'):
        x_max : int = 0
        y_max : int = 0
        v_max : int = 0
        for x in range(-1,1):
            for y in range(-1,1):
                vida : int = mundo.celulas[self._x + x][self._y + y].vida
                if  vida < v_max:
                    y_max = y
                    x_max = x
                    v_max = vida
        
        if x_max != 0 or y_max != 0:
            mundo.celulas[self._x][self._y] = Celula(_x = self._x, _y=self._y)
            self._x += x_max
            self._y += y_max
            mundo.celulas[self._x][self._y] = self
            print('yey')
            
            self.vida -= v_max
        vida -= 10
        return (0,min(255,int(255 * abs(self.vida)/400)),0)

def generar(x,y):
    if random.randint(0,6)>5:
        return CelulaViva(_x = x, _y = y)
    else:
        return Celula(_x = x, _y = y)

@dataclass(slots=True)
class Mundo(list):
    celulas : list[list[Celula]] = field(default_factory = lambda : [[generar(i,j) for j in range(100)] for i in tqdm(range(100))])

    def _step(self, SCREEN):
        blockSize = WINDOW_WIDTH / len(self.celulas)

        for cells_x in self.celulas:
            for cell_xy in cells_x:
                COLOR = cell_xy(self)
                pygame.draw.rect(SCREEN, COLOR, pygame.Rect(cell_xy._x*blockSize, cell_xy._y*blockSize, blockSize, blockSize))

    def __call__(self):
        print('Ejecucion')

        global SCREEN, CLOCK
        pygame.init()
        SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        SCREEN.fill(BLACK)
        CLOCK = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
            self._step(SCREEN)
            pygame.display.update()

    def __getitem__(self, items):
        return self.celulas[items]






def main():
    print('Empezamos')
    mundo : Mundo = Mundo()
    mundo()
    print('Terminamos')


if __name__ == "__main__":
    main()