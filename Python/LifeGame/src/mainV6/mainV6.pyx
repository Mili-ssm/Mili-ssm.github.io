# cython: infer_types=True
# cython: boundscheck=False
# cython: nonecheck=False
# cython: wraparound=False
# cython: overflowcheck=False
# cython: boundscheck=False
cimport cython
import numpy as np
cimport numpy as np
import pygame



cdef char[3] BLACK = (0, 0, 0)
cdef char[3] WHITE = (200, 200, 200)
cdef char[3] WHITE1 = (0, 0, 200)
cdef char[3] WHITE2 = (0, 200, 0)
cdef int WINDOW_HEIGHT = 1000
cdef int WINDOW_WIDTH = 1000

cdef unsigned short T = 3

cdef inline void recalculo(char[:,::1] matriz, char op, unsigned short x0, unsigned short x1, unsigned short x2, unsigned short prev_y):
    cdef unsigned short y
    cdef unsigned short i
    for i in range(T):
        y = prev_y+i
        matriz[x0,y] += op
        matriz[x1,y] += op
        matriz[x2,y] += op

cdef class Mundo():
    cdef unsigned short h
    cdef unsigned short w
    cdef char ciclo[2]
    cdef char[:,::1] celulas
    cdef char[:,::1] vecinosRead
    cdef char[:,::1] vecinosWrite
    def __cinit__(self, unsigned short size):
        self.ciclo = (0,1)
        self.h = size
        self.w = size
        self.vecinosWrite = np.zeros((self.h,self.w), dtype=np.ubyte)
        self.celulas = np.random.choice(np.asarray([0, 255],dtype=np.ubyte), size=(self.h,self.w), p=[4./5, 1./5])

        self.celulas[:,0] = 0
        self.celulas[0,:] = 0
        self.celulas[self.h-1,:] = 0
        self.celulas[:,self.w-1] = 0

        for x in range(self.w):
            for y in range(self.h):
                if self.celulas[x,y]:
                    recalculo(self.vecinosWrite, 1, x-1, x, x+1, y-1)
        self.vecinosRead = self.vecinosWrite.copy()

    cdef inline char[:,::1] step(self):
        cdef char[:,::1] celulas = self.celulas
        cdef char[:,::1] vecinosRead = self.vecinosRead
        cdef char[:,::1] vecinosWrite = self.vecinosWrite
        cdef unsigned short h = self.h
        cdef unsigned short w = self.w

        cdef unsigned short prev_x = 0
        cdef unsigned short prev_y = 0
        cdef unsigned short x
        cdef unsigned short y
        for x in range(1,w-1):
            for y in range(1,h-1):
                if celulas[x,y]:
                    if vecinosRead[x,y] > 4 or vecinosRead[x,y] < 3:
                        celulas[x,y] = 0
                        recalculo(vecinosWrite, -1,prev_x, x,x+1,prev_y)
                else:
                    if vecinosRead[x,y] == 3:
                        celulas[x,y] = 255
                        recalculo(vecinosWrite, 1,prev_x, x,x+1,prev_y)
            
                prev_y = y
            prev_y = 0
            prev_x = x

        self.vecinosRead = vecinosWrite.copy()
        self.vecinosWrite = vecinosWrite
        self.celulas = celulas
        return celulas

cdef class MOTOR():
    cdef char run

    cdef void exe(self, unsigned short size):
        cdef Mundo mundo = Mundo(size)
        self.run = True
        global SCREEN, CLOCK
        pygame.init()
        SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        CLOCK = pygame.time.Clock()

        SCREEN.fill((0, 0, 0))
        
        
        while self.run:
            CLOCK.tick()
            self.__Events__() 
                       
            
            SCREEN.blit(pygame.transform.scale(pygame.surfarray.make_surface(np.asarray(mundo.step())), (WINDOW_WIDTH, WINDOW_HEIGHT)), (0, 0))

            pygame.display.set_caption('Juego de Sant  -- FPS : {}'.format(CLOCK.get_fps()))
            pygame.display.flip()
        
        pygame.quit()

    
    cdef __Events__(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False





cpdef main(unsigned short size = 1000):
    print('Empezamos')
    motor : MOTOR = MOTOR()
    motor.exe(size)
    print('Terminamos')
