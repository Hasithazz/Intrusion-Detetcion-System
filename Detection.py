#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 21:19:37 2019

@author: hasitha
"""

from darkflow.net.build import TFNet
import cv2
import tensorflow as tf
import Identification
import time
import configparser

import os
cwd = os.getcwd()

print(cwd)

config_file = configparser.ConfigParser()
config_file.read('config.ini')

config = tf.ConfigProto(log_device_placement = True)
config.gpu_options.allow_growth = True 

with tf.Session(config=config) as sess:
    options = {
            'model': './cfg/yolo-intruder.cfg',
            'load': 400, 
            'threshold': 0.65,
            'gpu': 0.5
               }
    tfnet = TFNet(options)

cap = cv2.VideoCapture(0)
frame_number = 0
current_time = time.time()
print("started at - ", current_time)

config_file['TIMER']['START_TIME'] = str(current_time)
config_file['TIMER']['FIRST_RUN'] = str(1)
with open('config.ini', 'w') as configfile:    # save
    config_file.write(configfile)
    
while True:
    ret, frame = cap.read()
    start_time = time.time()
    frame_number += 1
    if ret:
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = tfnet.return_predict(img)
        #print(results)
        
        
        for (i, result) in enumerate(results):     
            x = result['topleft']['x']
            w = result['bottomright']['x']-result['topleft']['x']
            y = result['topleft']['y']
            h = result['bottomright']['y']-result['topleft']['y']
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            label_position = (x + int(w/2)), abs(y - 10)
            cv2.putText(frame, result['label'], label_position ,
                        cv2.FONT_HERSHEY_SIMPLEX,1, (255,0,0), 3)
            identify = Identification.Identification(result, frame)

        cv2.imshow("Objet Detection YOLO", frame)
        print("FPS: ", 1.0 / (time.time() - start_time))
        if cv2.waitKey(1) == 13: #13 is the Enter Key
            break

cap.release()
cv2.destroyAllWindows()

config_file['TIMER']['FIRST_RUN'] = str(1)
with open('config.ini', 'w') as configfile:    # save
    config_file.write(configfile)
    
