# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 10:16:22 2015

@author: lvanhulle
"""
import Point as p
#import InFill as infill
import Shape as s
import Line as l
import arc as a
import math
import numpy as np
import copy
import gcode as gc
import parameters as pr
import constants as c
import InFill as InF
from itertools import islice
import LineGroup as lg
import doneShapes as ds
import itertools
from operator import itemgetter
import time
import timeit
import matrixTrans as mt
import random
import bisect
import collections as col
from collections import Counter

#CW = -1
#CCW = 1
#
##X, Y = 0, 1
##
#arc = a.Arc(p.Point(49.642, 9.5), p.Point(28.5, 6.5), CW, p.Point(28.5, 82.5), 20)
##
#p1 = p.Point(2.073, 0.0806)
#p2 = p.Point(2.1512, 0.0323)
#p3 = p.Point(2.144081, 0.0389)
#p4 = p.Point(2.0251, 0.1612)
#p5 = p.Point(3,3.0001)
#p6 = p.Point(-1,0)
#p7 = p.Point(4,0)
#p8 = p.Point(4,4)
#p9 = p.Point(0,4)
#p10 = p.Point(3,12)
#p11 = p.Point(0,5)
#
#l1 = [p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11]
#
#ll = [l.Line(l1[i], l1[i+1]) for i in xrange(len(l1)-1)]
#
#nv = [pi.normalVector for pi in l1]
#
#s1 = ds.rect(0,0,10,10)#squareWithHole()
#
#l6 = ll[6]
#r1 = l.Line(p.Point(0,2), p.Point(1,2))
#r1f = r1.fliped()
#print 'Good: ' + str(l6.rayIntersects(r1))
#print 'Bad: ' + str(l6.rayIntersects(r1f))

s1 = ds.rect(0,0,10,12)
in1 = InF.InFill(s1, 2, 90)

s2 = ds.rect(2,2,6,8)

fieldStarts = in1.getStarts()
trimStarts = s2.getStarts()
Q_P = fieldStarts - trimStarts.reshape(4,1,2)

fieldVectors = in1.getVectors()
trimVectors = s2.getVectors()
denom = np.cross(trimVectors, fieldVectors.reshape(5,1,2))
all_t = np.cross(Q_P, trimVectors.reshape(4,1,2))/denom.reshape(4,5)



    
""" An example of how to do other infills. """  
#currOutline = ds.rect(0,0,15,250)
#filledList = []
#
#for shellNumber in range(pr.numShells):
#    filledList.append(currOutline)
#    currOutline = currOutline.offset(pr.pathWidth, c.INSIDE)
#
##pattern = lg.LineGroup()
##pattern.addLinesFromCoordinateList([[0,0],[2,2],[4,0]])
#infill = InF.InFill(currOutline, pr.pathWidth, pr.infillAngleDegrees)#, pattern)
#
#filledList.append(infill)
    
    