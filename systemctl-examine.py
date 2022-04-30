import os
from time import sleep
import time
import json
import re
from pushbullet import PushBullet

with open('auth.json') as data:
    data = json.load(data)
    pushbullet_token = data['pushbullet_token']
    sudopass = data['sudopass']
    
service = "shadowsocks-libev.service"
t = time.localtime()
pb = PushBullet(pushbullet_token)

def ctime():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return current_time

def status():
    a  = os.popen('systemctl status '+service).readlines()
    a = str(a)
    return a

cstart = 'sudo systemctl start '+service
cstop = 'sudo systemctl stop '+service
crestart = 'sudo systemctl restart '+service
wait1s= sleep(1)

while True:
    running = re.search(r'\b(running)\b',status())
    wait1s
    failed = re.search(r'\b(failed)\b',status())
    wait1s
    stop = re.search(r'\b(inactive)\b',status())
    wait1s
    
    if running:
        print ("Running")
        time.sleep(600) # 10 minutes
    elif failed:
        failedmes="Failed at " + ctime()+ '\nWill Be Starting Soon'
        push = pb.push_note("Skit Server", failedmes)
        sleep(2)
        p = os.system('echo %s|sudo -S %s' % (sudopass, crestart))
    elif stop:
        stopmes="Stop at " + ctime()+ '\nWill Be Starting Soon'
        push = pb.push_note("Skit Server", stopmes)
        sleep(2)
        p = os.system('echo %s|sudo -S %s' % (sudopass, crestart))
    else:
        unknownmes="Unknown Error at " + ctime()+ '\nWill Be Starting Soon'
        push = pb.push_note("Skit Server", unknownmes)
        sleep(2)
        p = os.system('echo %s|sudo -S %s' % (sudopass, crestart))
