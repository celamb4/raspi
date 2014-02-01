#!/usr/bin/env python

import pexpect #in case you want to read and communicate with arduino
import fdpexpect #for serial port
import serial #pyserial
import sys
import time
import string #useful string stuff
import subprocess
import os
import re  # useful string stuff for pexpect
import logging #for logging info and warnings
import smtplib #for sending emails when warning
import threading #used for creating threads
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import itertools
import datetime

##############################################################
##                  Functions defined here                  ##
##############################################################

port='/dev/ttyACM0' #port that arduino is plugged in to
global tank_temp, led_temp, blue, white #variables to monitor
global start
flag = False
start = 0

def Open_serial():
    global ser
    ser = serial.Serial(port,9600)
    ser.flushInput()
    time.sleep(1)


    global child
    fd = os.open(port, os.O_RDWR|os.O_NONBLOCK|os.O_NOCTTY)
    child = fdpexpect.fdspawn(fd) # Note integer fd is used instead of usual string.
    child.logfile_read = sys.stdout
    child.logfile_send = sys.stdout
    
def ping():
    retcode = subprocess.check_call(["ping", "-w 3", "www.google.com"])
    if retcode != 0:
        print "error no ping, will reboot now"
        net_reboot = subprocess.check_call(["sudo", "service", "network", "restart"])
        if net_reboot != 0:
            subprocess.call(["sudo", "reboot"])
    else:
        print "ping success"
        my_ip = subprocess.Popen(["curl", "ifconfig.me"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = my_ip.communicate()
        my_ip = output
        return my_ip

def blue_percent(w):
    dict = {'255':'0','240':'10','225':'20','210':'30','195':'40','180':'50','165':'60','150':'70','135':'80','120':'90','100':'100'}
    blue_per = dict[w]
    print dict[w],'%'
    return blue_per

def white_percent(w):
    dict = {'255':'0','242':'10','229':'20','216':'30','203':'40','190':'50','177':'60','164':'70','151':'80','138':'90','125':'100'}
    white_per = dict[w]
    print dict[w],'%'
    return white_per

def send_email(subject,var):
    my_ip = ping()
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = "cel.fishtank@gmail.com"
    msg["To"] = "ce.lambert4@gmail.com"
    msg["Cc"] = "claudia.grossi@gmail.com,ana.lambertg@gmail.com"
    body = MIMEText("Warning error occurred!! " + subject +": " + str(var) + '\r\n' + "Home IP: " +  my_ip)
    msg.attach(body)

        # Credentials (if needed)  
    username = 'cel.fishtank'
    password = 'rabbit2013'  
      
    # The actual mail send  
    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    session.ehlo()
    session.starttls()
    session.ehlo
    session.login(username, password)
    session.sendmail(msg["From"], msg["To"].split(",") + msg["Cc"].split(","), msg.as_string())
    session.quit()  

def ip_mail(subject):
    my_ip = ping()
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = "cel.fishtank@gmail.com"
    msg["To"] = "ce.lambert4@gmail.com"
    msg["Cc"] = ""
    body = MIMEText("Current IP is: " + my_ip)
    msg.attach(body)

        # Credentials (if needed)
    username = 'cel.fishtank'
    password = 'rabbit2013'

    # The actual mail send
    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    session.ehlo()
    session.starttls()
    session.ehlo
    session.login(username, password)
    session.sendmail(msg["From"], msg["To"].split(",") + msg["Cc"].split(","), msg.as_string())
    session.quit()


def trusty_sleep(n):
    start = time.time()
    while (time.time() - start < n):
        time.sleep(n - (time.time() - start))

def raise_flag():
    global start
    interval = 120
    if start > interval:
        start = 0
        flag = True
        return flag
    else:
        flag = False
        start = start + 1
        time.sleep(1)
        return flag


############################################################
##                       MAIN                             ##
############################################################

Open_serial()

while True:
 
    now = datetime.datetime.now()
    line = ser.readline()
    if line:
        tmp = line.split()
        if 'tank' in line:
            tank_temp = float(tmp[1])
            print 'Tank temperature:',tank_temp
            if tank_temp >= 27.00 and tank_temp != 85.00:
                print str(now)
                flag = raise_flag()
                if flag:
                    send_email('Tank temperature overheat',tank_temp)
                    flag = False
            elif tank_temp <= 24.00 and tank_temp != 85.00:
                print str(now)
                flag = raise_flag()
                if flag:
                    send_email('Tank temperature too low',tank_temp)
                    flag = False
                             
        if 'led' in line:
            led_temp = float(tmp[1])
            print 'Lights temperature:',led_temp
            if led_temp >= 40.00 and led_temp != 85.00:
                print str(now)
                flag = raise_flag()
                if flag:
                    send_email('Lights temperature Overheat',led_temp)
                    flag = False

        if 'White' in line:
            white_pwm = tmp[1]
            print 'White lights PWM value:',white_pwm
            white_per = white_percent(white_pwm)
            print 'White lights % value:',white_per

        if 'Blue' in line:
            blue_pwm = tmp[1]
            print 'Blue lights PWM:',blue_pwm
            blue_per = blue_percent(blue_pwm)
            print 'Blue lights % value:',blue_per

    if datetime.datetime.today().weekday() == 6:
        if datetime.datetime.now().minute == 30 and datetime.datetime.now().hour == 11:
            ip_mail('Fishtank IP')
            trusty_sleep(60)
        
    print str(now)
    time.sleep(1)
