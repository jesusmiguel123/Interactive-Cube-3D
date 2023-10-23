from itertools import product, cycle

from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
import pygame
import numpy as np

from .Wireframe import Wireframe

class ProjectionViewer:
    def __init__(self, width, height, actions, pX, pY, pZ, p1, p2, p3):
        self.width = width
        self.height = height
        self.actions = actions

        self.pX = pX
        self.pY = pY
        self.pZ = pZ

        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

        self.wireframes = Wireframe()

        pygame.init()
        pygame.display.set_mode(
            (self.width, self.height),
            DOUBLEBUF|OPENGL
        )
        pygame.display.set_caption('Cubo Rotado')
        pygame.key.set_repeat(1,10)

        self.clock = pygame.time.Clock()
        
        glMatrixMode(GL_PROJECTION)
        gluPerspective(60, (self.width/self.height), 0.1, 500)

        glMatrixMode(GL_MODELVIEW)
        glTranslate(0,0,-10)
        glRotatef(-45,0,1,0)
        glRotatef(25,1,0,-1)
        glPushMatrix()
        colors = np.random.random((24, 3))
        self.colors = cycle(colors)

    def addWireframe(self, wireframe):
        self.wireframes = wireframe

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_ESCAPE):
                        running = False
                    elif event.key in self.actions:
                        self.actions[event.key](self)

            self.display()

            glEnable(GL_DEPTH_TEST)
            
            orig_offset = np.array([0,0,0])
            orig_recta = np.array([self.p1,self.p2,self.p3])
            
            glLineWidth(7)

            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glBegin(GL_QUADS)
            glColor4f(0.3,0.3,0.3,0.5)
            glVertex3f(-10,0,-10)
            glVertex3f( 10,0,-10)
            glVertex3f( 10,0, 10)
            glVertex3f(-10,0, 10)
            glEnd()

            glBegin(GL_LINES)
            N = 10

            # X Red
            glColor(1,0,0)
            glVertex3fv(orig_offset)
            glVertex3fv(orig_offset + [N,0,0])
            
            glColor(1,0,0)
            glVertex3fv(orig_offset)
            glVertex3fv(orig_offset - [N,0,0])
            
            # Y Green
            glColor(0,1,0)
            glVertex3fv(orig_offset)
            glVertex3fv(orig_offset + [0,N,0])
            
            glColor(0,1,0)
            glVertex3fv(orig_offset)
            glVertex3fv(orig_offset - [0,N,0])
            
            # Z Blue
            glColor(0,0,1)
            glVertex3fv(orig_offset)
            glVertex3fv(orig_offset + [0,0,N])
            
            glColor(0,0,1)
            glVertex3fv(orig_offset)
            glVertex3fv(orig_offset - [0,0,N])

            # Axis
            glColor(0.6274,0.3137,0)
            glVertex3fv(orig_recta)
            glVertex3fv(
                orig_recta + [self.pX*N,self.pY*N,self.pZ*N]
            )

            glColor(0.6274,0.3137,0)
            glVertex3fv(orig_recta)
            glVertex3fv(
                orig_recta - [self.pX*N,self.pY*N,self.pZ*N]
            )
            
            glEnd()

            self.clock.tick(60)
            
            pygame.display.flip()
        pygame.quit()

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT |  GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        glColor(1,1,1)
        glLineWidth(1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        
        glBegin(GL_LINES) 
        for edge in self.wireframes.edges:
            ind1, ind2 = edge
            glVertex3fv(self.wireframes.nodes[ind1][:3])
            glVertex3fv(self.wireframes.nodes[ind2][:3])
        glEnd()
        
        glBegin(GL_QUADS) 
        for face in self.wireframes.faces: 
            for vert in face:
                col = next(self.colors)
                glColor(1,0,0)
                glVertex3fv(self.wireframes.nodes[vert][:3])
        glEnd()

        glPopMatrix()
        
    def translationMatrix(self, dx, dy, dz):
        return np.array([[1,0,0,0],
                         [0,1,0,0],
                         [0,0,1,0],
                         [dx,dy,dz,1]])

    def scaleMatrix(self, sx=0, sy=0, sz=0):
        return np.array([[sx, 0,  0,  0],
                         [0,  sy, 0,  0],
                         [0,  0,  sz, 0],
                         [0,  0,  0,  1]])

    def rotateXMatrix(self, radians):
        c = np.cos(radians)
        s = np.sin(radians)
        return np.array([[1, 0, 0, 0],
                         [0, c,-s, 0],
                         [0, s, c, 0],
                         [0, 0, 0, 1]])

    def rotateYMatrix(self, radians):
        c = np.cos(radians)
        s = np.sin(radians)
        return np.array([[ c, 0, s, 0],
                         [ 0, 1, 0, 0],
                         [-s, 0, c, 0],
                         [ 0, 0, 0, 1]])

    def rotateZMatrix(self, radians):
        c = np.cos(radians)
        s = np.sin(radians)
        return np.array([[c,-s, 0, 0],
                         [s, c, 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]])

    def translateAll(self, vector):
        glClear(GL_COLOR_BUFFER_BIT |  GL_DEPTH_BUFFER_BIT) #limpia buffer
        glEnable(GL_DEPTH_TEST)
        matrix = self.translationMatrix(vector[0], vector[1], vector[2])
        self.wireframes.transform(matrix)

    def scaleAll(self, scale):
        glClear(GL_COLOR_BUFFER_BIT |  GL_DEPTH_BUFFER_BIT) #limpia buffer
        glEnable(GL_DEPTH_TEST)
        centerF = (self.wireframes.nodes[0][:3] + self.wireframes.nodes[7][:3])/2
        center = [centerF[0], centerF[1], centerF[2], 0]
        matrix = self.scaleMatrix(scale, scale, scale)
        self.wireframes.scale(center, matrix)

    def rotateAll(self, axis, theta):
        glClear(GL_COLOR_BUFFER_BIT |  GL_DEPTH_BUFFER_BIT) #limpia buffer
        glEnable(GL_DEPTH_TEST)
        rotateFunction = 'rotate' + axis + 'Matrix'
        center = self.wireframes.findCentre()
        matrix = getattr(self, rotateFunction)(theta)
        self.wireframes.rotate(center, matrix)

    def rotateAxis(self, axis, theta):
        glClear(GL_COLOR_BUFFER_BIT |  GL_DEPTH_BUFFER_BIT) #limpia buffer
        glEnable(GL_DEPTH_TEST)
        rotateFunction = 'rotate' + axis + 'Matrix'
        matrix = getattr(self, rotateFunction)(theta)
        self.wireframes.transform(matrix)
        
    def rotateCAxis(self, theta):
        glClear(GL_COLOR_BUFFER_BIT |  GL_DEPTH_BUFFER_BIT) #limpia buffer
        glEnable(GL_DEPTH_TEST)
        a = self.pX
        b = self.pY
        c = self.pZ
        d = (b*b + c*c)**0.5
        Rt = np.array([[1, 0, 0, -self.p1],
                       [0, 1, 0, -self.p2],
                       [0, 0, 1, -self.p3],
                       [0, 0, 0,       1]])
        inRt = np.array([[1, 0, 0, self.p1],
                         [0, 1, 0, self.p2],
                         [0, 0, 1, self.p3],
                         [0, 0, 0, 1]])
        if(d != 0):
            Rx = np.array([[1, 0  , 0   , 0],
                           [0, c/d, -b/d, 0],
                           [0, b/d, c/d , 0],
                           [0, 0  , 0   , 1]])
            inRx = np.array([[1,    0,   0, 0],
                             [0,  c/d, b/d, 0],
                             [0, -b/d, c/d, 0],
                             [0,    0,   0, 1]])
            Ry = np.array([[d, 0, -a, 0],
                           [0, 1,  0, 0],
                           [a, 0,  d, 0],
                           [0, 0,  0, 1]])
            inRy = np.array([[ d, 0, a, 0],
                             [ 0, 1, 0, 0],
                             [-a, 0, d, 0],
                             [ 0, 0, 0, 1]])
            Rz = np.array([[np.cos(theta), -np.sin(theta), 0, 0],
                           [np.sin(theta),  np.cos(theta), 0, 0],
                           [0            ,  0            , 1, 0],
                           [0            ,  0            , 0, 1]])
            matrix = inRt.dot(inRx).dot(inRy).dot(Rz).dot(Ry).dot(Rx).dot(Rt)
        else:
            Ry = np.array([[d, 0, -a, 0],
                           [0, 1,  0, 0],
                           [a, 0,  d, 0],
                           [0, 0,  0, 1]])
            inRy = np.array([[ d, 0, a, 0],
                             [ 0, 1, 0, 0],
                             [-a, 0, d, 0],
                             [ 0, 0, 0, 1]])
            Rz = np.array([[np.cos(theta), -np.sin(theta), 0, 0],
                           [np.sin(theta),  np.cos(theta), 0, 0],
                           [0            ,  0            , 1, 0],
                           [0            ,  0            , 0, 1]])
            matrix = inRt.dot(inRy).dot(Rz).dot(Ry).dot(Rt)
        center = np.array([0, 0, 0, 0])
        self.wireframes.rotate(center, matrix)