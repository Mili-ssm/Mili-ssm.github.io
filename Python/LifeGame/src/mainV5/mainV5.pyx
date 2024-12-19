# cython: infer_types=True
import cython
from dataclasses import dataclass, field
import random
import numpy as np
cimport numpy as np
from tqdm import tqdm
import pygame



cdef char[3] BLACK = (0, 0, 0)
cdef char[3] WHITE = (200, 200, 200)
cdef char[3] WHITE1 = (0, 0, 200)
cdef char[3] WHITE2 = (0, 200, 0)
cdef int WINDOW_HEIGHT = 1000
cdef int WINDOW_WIDTH = 1000

@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline char comprobaciones(char[:,:] matriz):
    cdef int count = 0
    cdef char i = 0
    cdef char ii = 0
    for i in range(3):
        for ii in range(3):
            count += matriz[i][ii]
    return count == 3 or (matriz[1][1] and count==4)



cdef class Mundo():
    cdef int h
    cdef int w
    cdef char ciclo[2]
    cdef char[:,:,:] celulas
    cdef char[:,:,:] display
    def __cinit__(self, size):
        self.ciclo[0] = 0
        self.ciclo[1] = 1
        self.h = size
        self.w = size
        self.display = np.zeros((self.h,self.w,3), dtype=np.ubyte) 
        self.celulas = np.random.choice(np.asarray([0, 1],dtype=np.ubyte), size=(self.h,self.w,2), p=[4./5, 1./5])
        self.celulas[:,:,1] = 0
        self.celulas[0,:,0] = 0
        self.celulas[:,0,0] = 0
        self.celulas[self.h-1,:,0] = 0
        self.celulas[:,self.w-1,0] = 0

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cdef inline step(self):#, int BLOCKSIZE):
        cdef int int0 = self.ciclo[0]
        cdef int int1 = self.ciclo[1]

        cdef int prev_x = 0
        cdef int prev_y = 0
        cdef int x
        cdef int y
        for x in range(1,self.w-1):
            prev_y = 0
            for y in range(1,self.h-1):
                if comprobaciones(self.celulas[prev_x:x+1,prev_y:y+1,int0]):
                    if not self.celulas[x,y,int1]:
                        self.celulas[x,y,int1] = 1
                        self.display[x,y,:] = 200
                else:
                    if self.celulas[x,y,int1]:
                        self.celulas[x,y,int1] = 0
                        self.display[x,y,:] = 0
                prev_y = y
            prev_x = x


        self.ciclo[0] = int1
        self.ciclo[1] = int0

        return self.display

cdef class MOTOR():

    cdef exe(self, int size):
        cdef Mundo mundo = Mundo(size)

        global SCREEN, CLOCK
        pygame.init()
        SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        #SCREEN.fill(BLACK)
        CLOCK = pygame.time.Clock()


        
        #surf = pygame.transform.scale(surf, (WINDOW_WIDTH, WINDOW_HEIGHT))
        # draw the array onto the surface

        #cdef int blockSize = WINDOW_WIDTH / mundo.celulas.shape[1]
        #print(blockSize)
        while True:
            CLOCK.tick()
            self.__Events__()
            

            surf = pygame.Surface((mundo.h, mundo.w))
            pygame.surfarray.blit_array(surf, np.asarray(mundo.step()))
            surf = pygame.transform.scale(surf, (WINDOW_WIDTH, WINDOW_HEIGHT))
            SCREEN.fill((0, 0, 0))           
            SCREEN.blit(surf, (0, 0))

            pygame.display.set_caption('Juego de Sant  -- FPS : {}'.format(CLOCK.get_fps())) 
            pygame.display.flip()

    
    cdef __Events__(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()





cpdef main(int size):
    print('Empezamos')
    motor : MOTOR = MOTOR()
    motor.exe(size)
    print('Terminamos')
