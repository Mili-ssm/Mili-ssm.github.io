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



class Mundo(list):
    
    __slots__ =('h', 'w','ciclo','display','celulas')
    def __init__(self):
        self.h : int = SIZE
        self.w : int = SIZE
        self.ciclo :  np.ndarray[np.ubyte] = np.asarray((0,1))
        self.display : np.ndarray[np.ubyte] = np.zeros((SIZE,SIZE,3))
        self.celulas :  np.ndarray[np.ndarray[np.ubyte]] = np.random.choice((0, 1), size=(2,SIZE,SIZE), p=[4./5, 1./5])
        self.celulas[1] = 0
        self.celulas[0,0,:] = 0
        self.celulas[0,:,0] = 0
        self.celulas[0,SIZE-1,:] = 0
        self.celulas[0,:,SIZE-1] = 0


    def __call__(self):
        int0 = self.ciclo[0]
        int1 = self.ciclo[1]
        array0 = self.celulas[int0]
        array1 = self.celulas[int1]

        prev_x = 0
        for x in range(1,self.w-1):
            prev_y = 0
            for y in range(1,self.h-1):
                
                count : int = array0[prev_x:x+2,prev_y:y+2].sum()
                if  count == 3 or (array0[x,y] and count==4):
                    if not array1[x,y]:
                        array1[x,y] = 1
                        self.display[x,y,:] = 200
                else:
                    if array1[x,y]:
                        array1[x,y] = 0
                        self.display[x,y,:] = 0
                prev_y = y
            prev_x = x

        self.ciclo[0] = int1
        self.ciclo[1] = int0
        return self.display

@dataclass(slots=True)
class MOTOR():

    def __call__(self, mundo : Mundo = Mundo()):
        global SCREEN, CLOCK
        pygame.init()
        SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        CLOCK = pygame.time.Clock()

        while True:
            CLOCK.tick()
            self.__Events__()            

            surf = pygame.Surface((mundo.h, mundo.w))
            pygame.surfarray.blit_array(surf, mundo())
            surf = pygame.transform.scale(surf, (WINDOW_WIDTH, WINDOW_HEIGHT))
            SCREEN.fill((0, 0, 0))           
            SCREEN.blit(surf, (0, 0))

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