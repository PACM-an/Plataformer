import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random
import math

class Fake_Floors:
    
    #def __init__(self, x11, z11, x22, z22, x33, z33, x44, z44, la_Y):
    def __init__(self, x11, z11, x22, z22, la_Z, la_Y):
        #Se inicializa las coordenadas de los vertices del cubo
        self.vertexCoords = [  
                   1,1,1,   1,1,-1,   1,-1,-1,   1,-1,1,
                  -1,1,1,  -1,1,-1,  -1,-1,-1,  -1,-1,1  ]
        #Se inicializa los colores de los vertices del cubo
        self.vertexColors = [ 
                   1,1,1,   1,0,0,   1,1,0,   0,1,0,
                   0,0,1,   1,0,1,   0,0,0,   0,1,1  ]
        #Se inicializa el arreglo para la indexacion de los vertices
        self.elementArray = [ 
                  0,1,2,3, 0,3,7,4, 0,4,5,1,
                  6,2,1,5, 6,5,4,7, 6,7,3,2  ]

        #self.DimBoard = dim
        #Se inicializa una posicion aleatoria en el tablero
        self.Position = [0, 0, 0]
        #Se inicializa un vector de direccion aleatorio
        self.Direction = [0, 0, 0]
        
        # Pocición:
        self.x1 = x11 
        self.z1 = z11 
        self.x2 = x22 
        self.z2 = z22
        self.D_4ward = la_Z
        self.Up = la_Y

        
        

    #def update(self):
    #    x = 1
    
    def draw(self):
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glScaled(5,5,5)
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, self.vertexCoords)
        glColorPointer(3, GL_FLOAT, 0, self.vertexColors)
        glDrawElements(GL_QUADS, 24, GL_UNSIGNED_INT, self.elementArray)
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        glPopMatrix()

    def drawFace(self, x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4):
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(x1, y1, z1)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(x2, y2, z2)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(x3, y3, z3)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(x4, y4, z4)
        glEnd()
        
    def drawCube(self, texture, id):
        glPushMatrix()
        glTranslatef(0, 0, 0)
        glScaled(1,1,1)
        glColor3f(1.0, 1.0, 1.0)
        #Activate textures
        glEnable(GL_TEXTURE_2D)
        #front face
        glBindTexture(GL_TEXTURE_2D, texture[id])
        #self.drawFace(self.x1, self.Up, self.z1, self.x2, self.Up, self.z2, self.x3, self.Up, self.z3, self.x4, self.Up, self.z4)
        
        self.drawFace(self.D_4ward, self.Up, self.z2, self.D_4ward, self.Up, self.z1, self.x1, self.Up, self.z1, self.x2, self.Up, self.z2)
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()