#!/usr/bin/python

import sys, serial, time
from optparse import OptionParser

ser = serial.Serial('/dev/ttyACM0', 9600)

########################################
###           Check options          ###
########################################
opt = OptionParser()
opt.add_option('--status','-s',help='backlight status, OFF, ON, LED')
(options, args) = opt.parse_args()

#####################################
###         CHECK INPUTS          ###
#####################################
if options.status == None:
    options.status = raw_input('ON, OFF or LED:')
options.status = options.status.lower()

if options.status == 'on':
    byte = 1
    print 'light on'
elif options.status == 'off':
    byte = 0
    print 'light off'
elif options.status == 'led':
    byte = 2
    print 'turning LED for 2min'


print 'Input byte is "', byte

if byte == 1:
    print 'backlight ON'
    time.sleep(1)
    ser.write('1')

elif byte == 0:
    print 'backlight OFF'
    time.sleep(1)
    ser.write('0')

elif byte == 2:
    print 'countdown is 120'
    time.sleep(1)
    ser.write('2')
