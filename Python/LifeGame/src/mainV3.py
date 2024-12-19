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

    vida : int = field(default_factory=lambda: random.randint(-25, 25))

    def generar(x,y):
        if random.randint(0,6)>5:
            return Celula(_x = x, _y = y)
        else:
            return Celula(_x = x, _y = y)
            
    def __call__(self, mundo):
        for x in range(-1,1):
            for y in range(-1,1):
                self.vida += (20 * (mundo[self._x + x][self._y + y].vida/400))

        self.vida *=0.9

        if abs(self.vida) > 400:
            self.vida *= -0.3
        return (min(255,int(255 * max(self.vida,0)/400)),min(255,int(255 * max(-self.vida,0)/400)),0)



@dataclass(slots=True)
class Mundo(list):
    celulas : list[list[Celula]] = field(default_factory = lambda : [[Celula.generar(i,j) for j in range(200)] for i in tqdm(range(200))])

    def __call__(self, SCREEN, BLOCKSIZE):

        for cells_x in self.celulas:
            for cell_xy in cells_x:
                COLOR = cell_xy(self)
                pygame.draw.rect(SCREEN, COLOR, pygame.Rect(cell_xy._x*BLOCKSIZE, cell_xy._y*BLOCKSIZE, BLOCKSIZE, BLOCKSIZE))

    def __getitem__(self, items):
        return self.celulas[items]

@dataclass(slots=True)
class MOTOR():

    def __call__(self, mundo : Mundo = Mundo()):
        global SCREEN, CLOCK
        pygame.init()
        SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        SCREEN.fill(BLACK)
        CLOCK = pygame.time.Clock()


        blockSize = WINDOW_WIDTH / len(mundo.celulas)
        while True:
            CLOCK.tick()
            self.__Events__()
            mundo(SCREEN,blockSize)
            pygame.display.set_caption('Juego de Sant  -- FPS : {}'.format(CLOCK.get_fps()))
            pygame.display.flip()

    
    def __Events__(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()





def main():
    print('Empezamos')
    motor : MOTOR = MOTOR()
    motor()
    print('Terminamos')


if __name__ == "__main__":
    main()