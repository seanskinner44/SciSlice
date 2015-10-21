# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 09:51:36 2015

@author: lvanhulle
"""
import math
import numpy
import operator
numPoints = 20
CW = -1
CCW = 1
circle = [[2,0],[2,0],[CCW], [0,0]]
arc1 = [[49.642, 9.5], [28.5, 6.5], [CW],[28.5, 82.5]]
X, Y =0, 1
START = 0
END = 1
DIR = 2
CENTER = 3
INSIDE = 1
OUTSIDE = 0

tempShape1 = [[[]]]

def distance(first, second):
    return math.sqrt((first[X] - second[X])**2 + (first[Y] - second[Y])**2)

def calcIncludedAngle(start, end, direction):
    t = end - start
    if(direction == CW and t > 0):
        return t - 2*math.pi
    elif(direction == CCW and t < 0):
        return 2*math.pi+t
    elif(t == 0):
        return 2*math.pi
    else:
        return t

def mirror(lines, axis):
    if(axis == X):
        deltaX = 1
        deltaY = -1
    else:
        deltaX = -1
        deltaY = 1
    temp = [[c[X]*deltaX, c[Y]*deltaY] for c in lines]
    temp.reverse()
    return temp
    
def translate(shape, xShift, yShift):
    temp = [[c[X]+xShift, c[Y]+yShift] for c in shape]
    return temp

def arcToLineList(arc):
    radius = distance(arc[START], arc[CENTER])
    startAngle = math.atan2(arc[START] [Y]- arc[CENTER][Y],
                        arc[START] [X]- arc[CENTER][X])
    startAngle = startAngle if startAngle >= 0 else 2*math.pi+startAngle
    endAngle = math.atan2(arc[END] [Y]- arc[CENTER][Y],
                        arc[END] [X]- arc[CENTER][X])
    endAngle = endAngle if endAngle >= 0 else 2*math.pi+endAngle

    includedAngle = calcIncludedAngle(startAngle, endAngle, arc[DIR][0])
    currentAngle = startAngle
    tempList = [arc[START]]
    for i in range(numPoints-2):
        currentAngle += includedAngle/(numPoints-1)
        x = arc[CENTER][X]+radius*math.cos(currentAngle)
        y = arc[CENTER][Y]+radius*math.sin(currentAngle)
        tempList.append([x, y])
    tempList.append(arc[END])
#    print tempList
    return tempList
    
def areColinear(p1, p2, p3):
    if(p1[X] == p2[X] == p3[X]):#vertical line
        return True
    elif(p1[X] == p2[X] or p2[X] == p3[X]): #only one line is vertical       
        return False
    elif(abs((p2[Y]-p1[Y])/(p2[X]-p1[X]) - (p3[Y]-p2[Y])/(p3[X]-p2[X])) < 0.001): #the slope difference between P1P2 and P2P3 is less than an eror amount            
        return True
    return False
    
def removeDuplicates(lines):
    i = 0
    while i < (len(lines)-2):
        if(lines[i] == lines[i+1] or lines[i+1] == lines[i+2]):
            del lines[i+1]
        elif(areColinear(lines[i], lines[i+1], lines[i+2])):
            del lines[i+1]
        else:
            i += 1
    if(areColinear(lines[len(lines)-2], lines[len(lines)-1], lines[0])):
#        print 'here line 92'
        del lines[len(lines) - 1]
        del lines[0]
        lines.append(lines[0])
    return lines
    
def getLineAngle(p1, p2):
    angle = math.atan2((p2[Y]-p1[Y]), (p2[X] - p1[X]))
    return angle if angle >= 0 else angle + 2*math.pi
    
def isInside(point, shape):
    lowerPoint = [point[X], shape[0][Y]-10]
    intersections = 0
    for i in range(len(shape)-1):
        if(shape[i+1][Y] < lowerPoint[Y]): lowerPoint[Y] -= 10
#        print 'Point: ', point, ' LowerPoint: ', lowerPoint, ' shape[i]: ', shape[i], ' shape[i+1]: ', shape[i+1]   
        result, throwPoint =  segmentsIntersect(point, lowerPoint, shape[i], shape[i+1])
        if(result == 1):
            intersections += 1
    return (intersections % 2) #if intersections is even then the point was insdie, else it was outside
    
def offset(shape, dist, side):
    tempShape = [[]]
    line1Angle = getLineAngle(shape[0], shape[len(shape)-2])
    line2Angle = getLineAngle(shape[0], shape[1])
    halfAngle1 = (line1Angle + line2Angle)/2
    halfAngle2 = halfAngle1 + math.pi
    try1 = [shape[0][X] + dist*math.cos(halfAngle1), shape[0][Y] + dist*math.sin(halfAngle1)]
    try2 = [shape[0][X] + dist*math.cos(halfAngle2), shape[0][Y] + dist*math.sin(halfAngle2)]
    firstPoint = try1 if(isInside(try1, shape) == side) else try2
#    print 'Try1: ', try1, ' side: ', side, ' firstPoint: ', firstPoint
    tempShape[0] = firstPoint
    
    for i in range(1, len(shape)-1):
        line1Angle = getLineAngle(shape[i], shape[i-1])
        line2Angle = getLineAngle(shape[i], shape[i+1])
        halfAngle1 = (line1Angle + line2Angle)/2
        halfAngle2 = halfAngle1 + math.pi
        try1 = [shape[i][X] + dist*math.cos(halfAngle1), shape[i][Y] + dist*math.sin(halfAngle1)]
        try2 = [shape[i][X] + dist*math.cos(halfAngle2), shape[i][Y] + dist*math.sin(halfAngle2)]
        if(isInside(try1, shape)):
            tempShape.append(try1)
        elif(isInside(try2, shape)):
            tempShape.append(try2)              
                
    tempShape.append(firstPoint)
    return tempShape

def orderTwoNumbers(n1, n2):
    return ((n1, n2) if n1 < n2 else (n2, n1))

# a bounding box for a line segment is the upper left and lower right corners
# of the smallest box that encloses the line segment
def getBoundingBox(p1, p2):
    if(p1[Y] == p2[Y]):
        return ((p1, p2) if p1[X] < p2[X] else (p2, p1))
    if(p1[X] == p2[X]):
        return ((p1, p2) if p1[Y] > p2[Y] else (p2, p1))
    upperLeft = [None]*2
    lowerRight = [None]*2
    upperLeft[X], lowerRight[X] = orderTwoNumbers(p1[X], p2[X])
    lowerRight[Y], upperLeft[Y] = orderTwoNumbers(p1[Y], p2[Y])
    return (upperLeft, lowerRight)
    
    
def boundingBoxesIntersect(p1, p2, q1, q2):
    bb1 = getBoundingBox(p1, p2)
    bb2 = getBoundingBox(q1, q2)
#    print 'bb1: ', bb1
#    print 'bb2: ', bb2
    if(bb1[0][X] <= bb2[1][X] and
            bb1[1][X] >= bb2[0][X] and
            bb1[0][Y] >= bb2[1][Y] and
            bb1[1][Y] <= bb2[0][Y]):
                return True
    return False

# getOrientation takes in three points,
# returns 0 if they are colinear
# returns 1 if the turn is clockwise
# returns 2 if the turn is CCW
def getOrientation(p1, p2, p3):
    val = ((p2[Y] - p1[Y])*(p3[X] - p2[X]) - 
            (p2[X] - p1[X])*(p3[Y] - p2[Y]))
    if(val == 0): return 0 #colinear
    return (1 if val > 0 else 2)

def subtractPoints(p1, p2):
    return [p1[X] - p2[X], p1[Y] - p2[Y]]

def crossProductPoints(p1, p2):
#    print 'p1X: ', p1[X], ' p1Y: ', p1[Y], ' p2X: ', p2[X], ' p2Y: ', p2[Y]
    return float(p1[X]*p2[Y] - p1[Y]*p2[X])    

def matrixMultiply(matrix1, matrix2):
    if(len(matrix1[0]) != len(matrix2)):
        print 'matrix size error: matrixMultiply'
        return None
    result = [None] *len(matrix2)
    rowIndex = 0    
    for row in matrix1:
        add = 0
        for i in range(len(row)-1):
            add += row[i]*matrix2[i]
        result[rowIndex] = add
        rowIndex += 1
    return result
    
def pointToNormalVector(point):
    return [[point[X]], [point[Y]], [1.0]]
    
def normalVectorToPoint(nv):
    return [nv[X][0], nv[Y][0]]

def segmentsIntersect(p1, p2, q1, q2):
    if(not boundingBoxesIntersect(p1, p2, q1, q2)): return -1, None #return if bounding boxes do not intersetc
    o1 = getOrientation(p1, p2, q1)
    o2 = getOrientation(p1, p2, q2)
    o3 = getOrientation(q1, q2, p1)
    o4 = getOrientation(q1, q2, p2)
    
    if((o1+o2+o3+o4) == 0): return 0, None #return if all 4 points are colinear
    
    if(o1 != o2 and o3 != o4):
        r = subtractPoints(p2, p1)
        s = subtractPoints(q2, q1)
        Q_Less_P = subtractPoints(q1, p1)
        denom = crossProductPoints(r, s)
        t = crossProductPoints(Q_Less_P, s)/denom
        u = crossProductPoints(Q_Less_P, r)/denom
        if(abs(t) > 1 or abs(u) > 1):
            print 'Should we be here? segmentsIntersect math problem, I think'
#        print 't: ', t, ' u: ', u, ' r: ', r, ' s: ', s, ' Q_Less_P: ', Q_Less_P, ' Denom: ', denom
#        print 'P1: ', p1
        return 1, [p1[X]+r[X]*t, p1[Y]+r[Y]*t] #lines intersect at given point
    return -2, None #bounding boxes intersected but lines did not

#start from begining and compare from end
#When an intersection is found add the checked points to a list
#adjust the end points as needed on the new shape and the old
#recursively call the method with the old shape less the new shape  
#TODO: Does not handle a shape that intersects without forming a negative area
#or a shape that only forms a negative area without becoming positive again  
def intersectParser(shape, positiveArea):
    newShape = [[]]
    if(positiveArea): newShape[0] = shape[0]
    for i in range(len(shape)-2):
        point = []
        for j in range(len(shape)-2, i+2, -1):
            value, point = segmentsIntersect(shape[i], shape[i+1], shape[j], shape[j-1])
            if(value == 0): print 'Build something to handle this, intersectParser segments are co-linear'
            if(value == 1):
#                print 'Intersect Detected: ', point
                if(positiveArea):
                    newShape.append(point)
                    newShape.extend(shape[j:len(shape)])
                tempShape = [[]]
                tempShape[0] = point
                tempShape.extend(shape[i+1:j])
                tempShape.append(point)
                index = intersectParser(tempShape, not positiveArea)
                if(newShape != [[]]):
                    tempShape1.append(newShape)
                    return index+1
                return index
        if(positiveArea):
            newShape.append(shape[i+1])
    tempShape1[0] = newShape
    return 1
    
def getshapeMinMax(shape):
    minX = shape[0][X]-5
    maxX = minX+10
    minY = shape[0][Y]-5
    maxY = minY+10
    
    for point in shape:
        if(point[X] < minX): minX = point[X]-5
        elif(point[X] > maxX): maxX = point[X]+5
        if(point[Y] < minY): minY = point[Y]-5
        elif(point[Y] > maxY): maxY = point[Y]+5
    return minX, maxX, minY, maxY

def setOfLines(lineSpace, lineAngle, insideShape):
    lineSet = [[[]]]
    minX, maxX, minY, maxY = getshapeMinMax(insideShape)
    maxDiagonal = distance([minX, minY], [maxX, maxY])+4*lineSpace
    centerX = (maxX-minX)/2.0 + minX
    centerY = (maxY-minY)/2.0 + minY
    leftX = centerX-maxDiagonal/2.0
    rightX = centerX+maxDiagonal/2.0
    lineSet[0] = [[leftX, centerY, 1], [rightX, centerY, 1]]
    numSteps = int(maxDiagonal/2.0/lineSpace)
    for i in range(1, numSteps):
        lineSet.append([[leftX, centerY+i*lineSpace], [rightX, centerY+i*lineSpace]])
        lineSet.append([[leftX, centerY-i*lineSpace], [rightX, centerY-i*lineSpace]])
    lineSet = sorted(lineSet, key = lambda line : line[0][1])
    R = [[math.cos(lineAngle), -math.sin(lineAngle)], [math.sin(lineAngle), math.cos(lineAngle)]]
    p = [[centerX], [centerY]]
#    print "p: ", p
    p_lessRp = numpy.subtract(p, numpy.dot(R, p))
#    print 'p_lessRp: ', p_lessRp
    T = [[0 for x in range(3)] for x in range(3)]
    
    for i in range(2):
        for j in range(2):
            T[i][j] = R[i][j]
    T[0][2] = p_lessRp[0][0]
    T[1][2] = p_lessRp[1][0]
    T[2][2] = 1.0
    
#    print 'T: ', T
#    print 'lineSet[0][0]: ', lineSet[0][0]
#    print 'lineSet[0][1]: ', lineSet[0][1]
#    pTNV = pointToNormalVector(lineSet[0][0])
#    print 'pointToNormalVector: ', pointToNormalVector(lineSet[0][0])
#    print 'dot: ', numpy.dot(T, pTNV)
    for i in range(len(lineSet)):
        normalVector1 = numpy.dot(T, pointToNormalVector(lineSet[i][0]))
        normalVector2 = numpy.dot(T, pointToNormalVector(lineSet[i][1]))
        lineSet[i][0] = normalVectorToPoint(normalVector1)
        lineSet[i][1] = normalVectorToPoint(normalVector2)
    
#    for line in lineSet:
#        print line
    return lineSet   

def getMidPoint(line):
    x = (line[0][X] - line[1][X])/2.0 + line[1][X]
    y = (line[0][Y] - line[1][Y])/2.0 + line[1][Y]
    return ([x, y])

#create a multi point line, start, end, intersect point
#then sort by XY, then create seperate line segments, then check if in middle
#maybe make newLines[[]] the list of line segments and then put the lines in finalLines[[]]
def trimBackground(background, outline):
    newLines = [[]]
    offset = 1
    for line in background:
        newLines.append([line[0]]) #add first point of line to last line in newLines
        for i in range(len(outline)-1):
            value, point = segmentsIntersect(line[0], line[1], outline[i], outline[i+1])
            if(value == 1):
                newLines[offset].append(point)
                offset += 1
                newLines.append([point])
        newLines[offset].append(line[1])
        offset += 1
    newLines.pop(0)
#    for line in newLines:
#        print line
        
    finalLines = [[]]
#TODO: Sort line then check midpoint then add to finalLines[[]]
    for line in newLines:
        if(isInside(getMidPoint(line), outline)):
            finalLines.append(line)
    finalLines.pop(0)    
    return finalLines

def linesToPath(lineSet):
    reverse = False
    path = [[]]
    for line in lineSet:
        if(reverse):
            path.append(line[1])
            path.append(line[0])
        else:
            path.append(line[0])
            path.append(line[1])
        reverse = not reverse
    path.pop(0)
    return path

    

dogBone = [[82.5, 0], [82.5, 9.5], [49.642, 9.5]]
dogBone.extend(arcToLineList(arc1))
dogBone.append([0,6.5])
dogBone.extend(mirror(dogBone, Y))
dogBone.extend(mirror(dogBone, X))

dogBone = removeDuplicates(dogBone)
dogBone = translate(dogBone, 120, 60)


#print dogBone
#for c in dogBone:
#    print'X{:.3f} Y{:.3f}'.format(c[X],c[Y])

#print segmentsIntersect([1,1], [3,3], [4,2], [3,3])


fullPath = [[[]]]
fullPath[0] = dogBone

#numOffsets = 18

beadWidth = 0.501
airGap = 0.0
ZStep = 0.4
ZHeight = 3.201
extrusionRate = 0.017*1.75 #mm of extrusion per mm of XY travel
travelSpeed = 2000 #mm per min


stepOver = beadWidth+airGap
numZSteps = int(ZHeight/ZStep)

background = setOfLines(stepOver, math.pi/2, dogBone)

#list1 = [[1,2], [2,1],[5,6], [2,3]]

#list1 = sorted(list1, key = operator.itemgetter(0,1))

#print list1

background = trimBackground(background, dogBone)

#for line in fillPattern:
#    for point in line:
#        print '{:.3f}\t{:.3f}'.format(point[X],point[Y])
        
pathPoints = linesToPath(background)

pathPoints.reverse()

#for point in pathPoints:
#    print '{:.3f}\t{:.3f}'.format(point[X],point[Y])
              
f = open('PathFile2.txt', 'w')
f.write('G90 G21\n')

lineNumber = 1
totalExtrusion = 0
for level in range(1, numZSteps+1):
    f.write('\n; Level {:.0f} Z Height {:.3f}\n'.format(level, (level*ZStep)))
    f.write(';T{:.0f}\n'.format(level))
    f.write(';M6\n')
    f.write('G01 Z{:.3f} F{:.0f}\n'.format((level*ZStep+10), travelSpeed))
    f.write('G00 X{:.3f} Y{:.3f}\n'.format(pathPoints[0][X], pathPoints[0][Y]))
    f.write('G01 Z{:.3f} F{:.0f} E{:.3f}\n'.format((level*ZStep), (travelSpeed/2), totalExtrusion))
    
    for i in range(len(pathPoints)-1):
        f.write('G01 X{:.3f} Y{:.3f} '.format(pathPoints[i+1][X], pathPoints[i+1][Y]))
        f.write('F{:.0f} '.format(travelSpeed))
        extrusionAmount = extrusionRate * distance(pathPoints[i], pathPoints[i+1])
        totalExtrusion += extrusionAmount
        f.write('E{:.3f}\n'.format(totalExtrusion))     
        
    f.write('G01 Z{:.3f} F{:.0f} E{:.3f}\n'.format(((level+1)*ZStep+10), travelSpeed, (totalExtrusion-1)))

f.write('M30\n')
f.close()
print 'Done writing File.'  

"""
for loop in fullPath:
    f.write('(Loop Number {:.0f})\n'.format(loopNumber))
    f.write('T{:.0f}\nM6\n'.format(loopNumber))
    loopNumber += 1
    for point in loop:
        f.write('N{:.0f} X{:.3f} Y{:.3f}\n'.format(lineNumber, point[X],point[Y]))
        lineNumber+=1

for i in range(numOffsets):
    holdPath = offset(fullPath[i], beadWidth+airGap, INSIDE)
    if(intersectParser(holdPath, True) == 1):
        fullPath.append(holdPath)
    else:
        for path in tempShape1:
            fullPath.append(path)
            for j in range(i, numOffsets):
                fullPath.append(offset(fullPath[len(fullPath)-1], beadWidth+airGap, INSIDE))
        break
"""
