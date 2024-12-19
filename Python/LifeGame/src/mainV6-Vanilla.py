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

SIZE = 500



class Mundo(list):
    
    __slots__ =('h', 'w','ciclo','celulas','vecinos')
    def __init__(self):
        self.h : int = SIZE
        self.w : int = SIZE
        self.ciclo :  np.ndarray[np.ubyte] = np.asarray((0,1))
        self.vecinos = np.zeros((2,self.h,self.w), dtype=np.ubyte)
        self.celulas :  np.ndarray[np.ndarray[np.ubyte]] = np.random.choice((0, 1), size=(SIZE,SIZE), p=[4./5, 1./5])
        self.celulas[0,:] = 0
        self.celulas[:,0] = 0
        self.celulas[SIZE-1,:] = 0
        self.celulas[:,SIZE-1] = 0

        for x in range(self.w):
            for y in range(self.h):
                if self.celulas[x,y]:
                    self.vecinos[0,x-1:x+2,y-1:y+2] += 1
        self.vecinos[1] = self.vecinos[0]


    def __call__(self):

        prev_x = 0
        for x in range(1,self.w-1):
            prev_y = 0
            for y in range(1,self.h-1):
                
                estado = self.celulas[x,y]
                vecinos : int = self.vecinos[0,x,y]
                if  vecinos == 3 or (estado and vecinos==4):
                    if not estado:
                        self.celulas[x,y] = 1
                        self.vecinos[1,prev_x:x+2,prev_y:y+2] += 1
                else:
                    if estado:
                        self.celulas[x,y] = 0
                        self.vecinos[1,prev_x:x+2,prev_y:y+2] -= 1
                prev_y = y
            prev_x = x

        
        self.vecinos[0] = self.vecinos[1]
        return self.celulas * 255

@dataclass(slots=True)
class MOTOR():

    def __call__(self, mundo : Mundo = Mundo()):
        global SCREEN, CLOCK
        pygame.init()
        SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        CLOCK = pygame.time.Clock()

        SCREEN.fill((0, 0, 0))
        while True:
            CLOCK.tick()
            self.__Events__()            

            SCREEN.blit(pygame.transform.scale(pygame.surfarray.make_surface(np.asarray(mundo())), (WINDOW_WIDTH, WINDOW_HEIGHT)), (0, 0))

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