# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 13:13:34 2015

@author: lvanhulle
"""
import numpy
import math
from parameters import constants as c
class Point:
    
    COMPARE_PRECISION = 10000
    
    def __init__(self, x, y=None, z=0):
        self._x = x
        self._y = y
        self._z = z
        self.normalVector = numpy.array([x, y, z, 1])
        
    @property
    def x(self):
        return self._x
        
    @property
    def y(self):
        return self._y
    
    @property
    def z(self):
        return self._z
    
    def __iter__(self):
        return(i for i in (self.x, self.y, self.z))
    
    def get2DPoint(self):
        return [self.x, self.y]

    def mirror(self, axis):
        transMatrix = numpy.identity(4)
        if(axis == c.X):
            transMatrix[c.Y][1] = -1
        else:
            transMatrix[c.X][0] = -1
        return self.transform(transMatrix)
    
    def rotate(self, angle, point):
        if(point is None): point = Point(0,0)
        toOrigin = numpy.identity(4)
        toOrigin[c.X][3] = -point.x
        toOrigin[c.Y][3] = -point.y
        
        rotateMatrix = numpy.identity(4)
        rotateMatrix[c.X][0] = math.cos(angle)
        rotateMatrix[c.Y][0] = math.sin(angle)
        rotateMatrix[c.X][1] = -rotateMatrix[c.Y][0]
        rotateMatrix[c.Y][1] = rotateMatrix[c.X][0]
        
        transBack = numpy.identity(4)
        transBack[c.X][3] = point.x
        transBack[c.Y][3] = point.y
        
        transMatrix = numpy.dot(transBack, numpy.dot(rotateMatrix, toOrigin))
        return self.transform(transMatrix)
    
    def translate(self, shiftX, shiftY, shiftZ=0):
        transMatrix = numpy.identity(4)
        transMatrix[c.X][3] = shiftX
        transMatrix[c.Y][3] = shiftY
        transMatrix[c.Z][3] = shiftZ
        return self.transform(transMatrix)
        
    def transform(self, transMatrix):
        nv = numpy.dot(transMatrix, self.normalVector)
        return Point(nv[c.X], nv[c.Y], nv[c.Z])
        
    def distance(self, other):
        return numpy.linalg.norm(self.normalVector - other.normalVector)
        
    def squareDistance(self, other):
        return ((self.x - other.x)**2 + (self.y - other.y)**2)

    def __key(self):
        return(int(round(self.z*self.COMPARE_PRECISION)), int(round(self.x*self.COMPARE_PRECISION)),
               int(round(self.y*self.COMPARE_PRECISION)))
    
    def __lt__(self, other):
        return self.__key() < other.__key()
        
    def __gt__(self, other):
        return self.__key() > other.__key()

    def __eq__(self, other):
        return self.__key() == other.__key()
        
    def __ne__(self, other):
        return self.__key() != other.__key()
        
    def __hash__(self):
        return hash(self.__key())
    
    def __str__(self):
        return 'X{:.3f} Y{:.3f} Z{:.3f}'.format(self.x, self.y, self.z)
    
    def getNormalVector(self):
        nv = [n for n in self.normalVector]
        return nv
        
    