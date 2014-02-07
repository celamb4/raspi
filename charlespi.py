#!/usr/bin/env python

import cgi
import cgitb; cgitb.enable()
import os, time

log = "/var/log/supervisor/arduinoser.log"
f = open(log,"r")

#Find the size of the file and move to the end
st_results = os.stat(log)
st_size = st_results[6]
file.seek(st_size)

where = file.tell()
line = f.readline()
if line:
    if 'tank' in line:
        tank_temp = line

    if 'led' in line:
        led_temp = line

if not line:
    time.sleep(5)
    file.seek(where)

print "Content-type:text/html\r\n\r\n"
print '<html>'
print '<head>'
print '<title>Charles Pi - Fishtank</title>'
print '</head>'
print '<body>'
print '<h2>Current status</h2>'
print line
if tank_temp:
    print tank_temp
if led_temp:
    print led_temp
print '</body>'
print '</html>'
