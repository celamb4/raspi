#!/usr/bin/env python

import os, re, subprocess, time, sys

##############################################################
##                  Functions defined here                  ##
##############################################################
def findThisProcess( process_name ):
    ps = subprocess.Popen("ps aux | grep -v grep | grep "+process_name, shell=True, stdout=subprocess.PIPE)
    output = ps.stdout.read()
    ps.stdout.close()
    ps.wait()
    return output

def isThisRunning( process_name ):
    output = findThisProcess( process_name )
    print output
    if re.search(process_name, output) is None:
      return False
    else:
      return True

############################################################
##                       MAIN                             ##
############################################################

while True:
    if isThisRunning('arduino') == False:
        print("Not running")
        p = subprocess.Popen([sys.executable, '/home/pi/scripts/serial_arduino.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        time.sleep(10)
    else:
        print("Running!")

    time.sleep(10)
