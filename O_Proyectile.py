import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random
import math

class Balls:
    
    def __init__(self, x11, z11, y11, m):

        #self.DimBoard = dim
        #Se inicializa una posicion aleatoria en el tablero
        self.Position = [0, 0, 0]
        
        #Se inicializa un vector de direccion aleatorio
        self.Direction = [2, 0, 0]
        
        # Pocición:
        self.Position[0] = x11
        self.Position[1] = z11
        self.Position[2] = y11
        self.m = m
        #self.m2 = m2
        angulo = math.radians(m)
        new_x = math.cos(angulo)*self.Direction[0] + math.sin(angulo)*self.Direction[2]
        new_z = - math.sin(angulo)*self.Direction[0] + math.cos(angulo)*self.Direction[2]
        self.Direction[0] = new_x
        self.Direction[2] = new_z
        self.foward = 0
        
    def doxxeo(self):
        return [int(self.Position[0]), int(self.Position[1]), int(self.Position[2])]
        
    def drawCube(self, sphere):
        #self.foward = self.foward + 1
        self.Position[0] = self.Position[0] + self.Direction[0]
        self.Position[2] = self.Position[2] + self.Direction[2]
        glPushMatrix()
        glColor3f(0.0,1.0,0.0)
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        #glTranslatef(self.x1 + self.dir[0], self.z1 + self.dir[2], self.y1)
        #glRotatef(self.m, 0.0, 1.0, 0.0) # Girar mov
        #glTranslatef(self.foward,0.0,0.0)
        glScalef(2,2,2)
        gluSphere(sphere, 1.0, 32, 16)
        glPopMatrix()