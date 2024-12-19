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

SIZE = 200

def comprobaciones(matriz) -> bool:
    count : int = matriz.sum()
    if count == 3 or (matriz[1][1] and count==4):
        return 1
    else:
        return 0



@dataclass(slots=True)
class Mundo(list):
    h : int = SIZE
    w : int = SIZE
    celulas :  np.ndarray[np.ndarray[np.bool]] = field(default_factory = lambda : np.random.choice([0, 1], size=(2,SIZE,SIZE), p=[1./3, 2./3]))
    ciclo :  np.ndarray[np.bool] = field(default_factory = lambda : np.asarray([0,1]))

    def __call__(self, SCREEN, BLOCKSIZE):
        int0 = self.ciclo[0]
        int1 = self.ciclo[1]
        array0 = self.celulas[int0]
        array1 = self.celulas[int1]

        for x in range(1,self.w-1):
            for y in range(1,self.h-1):
                resp = comprobaciones(array0[x-1:x+2,y-1:y+2])
                if resp:
                    pygame.draw.rect(SCREEN, WHITE, pygame.Rect(x*BLOCKSIZE, y*BLOCKSIZE, BLOCKSIZE, BLOCKSIZE))
                else:
                    pygame.draw.rect(SCREEN, BLACK, pygame.Rect(x*BLOCKSIZE, y*BLOCKSIZE, BLOCKSIZE, BLOCKSIZE))
                array1[x][y] = resp


        self.ciclo[0] = int1
        self.ciclo[1] = int0

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


        blockSize = WINDOW_WIDTH / mundo.celulas.shape[1]
        print(blockSize)
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