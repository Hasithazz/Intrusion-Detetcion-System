#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 22:09:32 2019

@author: hasitha
"""

import cv2
import configparser
import time
    
config = configparser.ConfigParser()
config.read("config.ini")

start_time = config['TIMER']['START_TIME']
interval = config['TIMER']['INTERVAL']
file = config['PATH']['SAVE_IMG']



class Identification:

    def __init__(self, detectedObjects,img):        
        
        self.detectedObjects = detectedObjects
        self.image = img
        threatLevel = Identification.generateThreatLevel(self)
        self.informUser(threatLevel)
        
    def generateThreatLevel(self):        
        threatLevel = 0
        
        if(self.detectedObjects['label'] == 'intruder'):
            threatLevel += 10
            self.saveImage()
        return threatLevel
        
    def informUser(self,threatLevel):
        if threatLevel >= 8:
            import CommunicationHandler
            communicationHandler = CommunicationHandler.CommunicationHandler()
    
    def saveImage(self):    
        first_run = config['TIMER']['FIRST_RUN']
        print(first_run)
        print('this is file --->',file)
        
        if(first_run == '1'):
            print('Saving Image ..............')
            status = cv2.imwrite(file,self.image)
            print('File is saved = ',status)
        
        if((time.time()-float(start_time))%(float(interval)*60) == 0):
            cv2.imwrite(file,self.image)
            print('File is saved = ',status)