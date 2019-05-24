#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  2 02:57:09 2019

@author: hasitha
"""
import configparser
import EmailHandler
import time

config = configparser.ConfigParser()
config.read("config.ini")

class CommunicationHandler:
    
    def __init__(self):        
        type = config['COMMUNICATION']['TYPE']               
        
        if(type == 'email'):
            CommunicationHandler.callEmailHandler()
            
        
    def callEmailHandler():
        receiver = config['EMAIL']['RECEIVER']
        subject = config['CONTENT']['SUBJECT']
        message = config['CONTENT']['MESSAGE']
        start_time = config['TIMER']['START_TIME']
        interval = config['TIMER']['INTERVAL']
        first_run = config['TIMER']['FIRST_RUN']
        
        handler = EmailHandler.EmailHandler(receiver, subject, message)
        
        if(first_run == '1'):
            handler.display_message()
            print("Sending Email.......")
            handler.send_mail()
            config['TIMER']['FIRST_RUN'] = str(2)
            with open('config.ini', 'w') as configfile:    # save
                config.write(configfile)
            
        
        if((time.time()-float(start_time))%(float(interval)*60) == 0):
            print("1 minute passed")     
            print("Sending Email.......")
            handler.display_message()
            handler.send_mail()

