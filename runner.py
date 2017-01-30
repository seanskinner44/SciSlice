# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 13:12:35 2016
@author: adiebold
"""

import figura as fg
from gcode import Gcode, RobotCode
import time
from parameters import makeParamObj
import json
import constants as c
import os

class Runner:
    
    def __init__(self, jsonName, outputFileName, gRobot, jsonPath, layerParamLabels, partParamLabels):
        self.outputFileName = outputFileName
        with open(jsonName, 'r') as fp:
            data = json.load(fp)

        self.pr = makeParamObj(data[0], data[1], data[2:], jsonPath, layerParamLabels, partParamLabels)
        if gRobot == c.GCODE:
            self.gc = Gcode(self.pr)
        elif gRobot == c.ROBOTCODE:
            self.gc = RobotCode(self.pr)
    
    def run(self):
        startTime = time.time()
        print('\nGenerating code, please wait...')
        
        fig = fg.Figura(self.pr, self.gc)

        with open(self.outputFileName, 'w') as f:
            for string in fig.masterGcode_gen():
                f.write(string)
        
        endTime = time.time()
        print('\nCode generated.')
        print('Done calculating: ' + self.outputFileName + '\n')
        print('{:.2f} total time'.format(endTime - startTime))
        return fig.data_points
        """
        if c.LOG_LEVEL < c.logging.WARN:
            with open(self.outputSubDirectory+'\\'+self.outputFileName, 'r') as test,\
                 open(self.outputSubDirectory+'\\SAVE_master.gcode') as master:
                testLines = test.readlines()
                masterLines = master.readlines()
                i = 0
                numDiffs = 0
                for t,m in zip(testLines, masterLines):
                    i += 1
                    if t != m:
                        numDiffs += 1
                        if i%10**round(np.log10(i*2)-1)<1:
                            print('Diff at line: ', i)
                            print('Test: ' + t)
                            print('Master: ' + m)
                            print('---------------------------\n')
            print('\nTotal number of differences: ', numDiffs)
        """


           