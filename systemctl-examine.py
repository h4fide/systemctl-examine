try:
    import os
    import sys
    from time import sleep
    import time
    import re
    from auth import pushbullet_token, sudopass
except ImportError as e: 
    print('You need to install missing libraries\n')
    sys.exit(e)
    

try:
    from pushbullet import PushBullet
except ImportError as e:
    print('Required Pushpullet Library - !Not installed!')
    u_input = input(' Hit [Enter] to install Pushbullet ')
    if u_input == '':
        os.system("pip install pushbullet.py")
    else:
        sys.exit('Abandon!')
  
with open('auth.json') as data:
    data = json.load(data)
    pushbullet_token = data['pushbullet_token']
    sudopasswd = data['sudo_password']
    
service = "shadowsocks-libev.service" # choose systemctl service
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

while True:
    running = re.search(r'\b(running)\b',status())
    sleep(1)
    failed = re.search(r'\b(failed)\b',status())
    sleep(1)
    stop = re.search(r'\b(inactive)\b',status())
    sleep(1)
    
    if running:
        print ("Running")
        time.sleep(600) # 10 minutes
    elif failed:
        failedmes="Failed at " + ctime()+ '\nWill Be Starting Soon'
        push = pb.push_note("Skit Server", failedmes)
        sleep(2)
        p = os.system('echo %s|sudo -S %s' % (sudopasswd, crestart))
    elif stop:
        stopmes="Stop at " + ctime()+ '\nWill Be Starting Soon'
        push = pb.push_note("Skit Server", stopmes)
        sleep(2)
        p = os.system('echo %s|sudo -S %s' % (sudopasswd, crestart))
    else:
        unknownmes="Unknown Error at " + ctime()+ '\nWill Be Starting Soon'
        push = pb.push_note("Skit Server", unknownmes)
        sleep(2)
        p = os.system('echo %s|sudo -S %s' % (sudopasswd, crestart))
