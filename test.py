#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 06:16:57 2019

@author: hasitha
"""
import cv2
from darkflow.net.build import TFNet
import numpy as np
import time
import tensorflow as tf

config = tf.ConfigProto(log_device_placement = True)
config.gpu_options.allow_growth = True 
options = {"model": "./cfg/yolo-intruder.cfg", 
           "load": "./bin/yolo.weights",
           "batch": 8,
           "epoch": 500,
           "gpu": 1.0,
           "train": True,
           "annotation": "train/annotations/",
           "dataset": "train/images/"}
           
tfnet = TFNet(options)
tfnet.train()

options = {"model": "yolo-intruder.cfg",
           "load": -1,
           "gpu": 1.0}

import os
cwd = os.getcwd()

print(cwd)
      
tfnet2 = TFNet(options)
tfnet2.load_from_ckpt()

file_name = './sample_img/16' + '.jpg'
img = cv2.imread(file_name)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
results = tfnet2.return_predict(img)
img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
for (i, result) in enumerate(results):
    x = result['topleft']['x']
    w = result['bottomright']['x']-result['topleft']['x']
    y = result['topleft']['y']
    h = result['bottomright']['y']-result['topleft']['y']
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    label_position = (x + int(w/2)), abs(y - 10)
    cv2.putText(img, result['label'], label_position , cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,255,0), 2)

cv2.imshow("Objet Detection YOLO", img)
cv2.waitKey(0)
cv2.destroyAllWindows()