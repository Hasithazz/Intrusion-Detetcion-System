#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 04:37:15 2019

@author: hasitha
"""
import smtplib
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

class EmailHandler:
    
    def __init__(self, reciver_email, subject, message):
        self.reciver_email = reciver_email
        self.subject = subject
        self.message = message
    
    def display_message(self):
        print(self.message)

    sender = config['EMAIL']['EMAIL_ADDRESS']#'realzubzero@gmail.com'
    password = config['EMAIL']['PASSWORD']
    path = config['PATH']['SAVE_IMG']
    

    def send_mail(self):
        
        msg = MIMEMultipart()
        msg['From'] = self.sender
        msg['To'] = self.reciver_email
        msg['Subject'] = self.subject       
        
        attachment = open(self.path, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= "+self.path)
        
        msg.attach(part)
        msg.attach(MIMEText(self.message,'plain'))
        text = msg.as_string()
        
        print("Sending......")
        mail = smtplib.SMTP('smtp.gmail.com',587)
        
        mail.ehlo()
        mail.starttls()
    
        mail.login(self.sender, self.password)
        mail.sendmail(self.sender, self.reciver_email, text)
        mail.quit()
    
    
