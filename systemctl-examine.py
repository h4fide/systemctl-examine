import os
import time
from subprocess import run
import json
import re
from dhooks import Webhook, File, Embed
#discord
message = "Application Stopped \nWill Be Back Now"
with open('data.json', encoding='utf-8') as json_data:
    data = json.load(json_data)
sudo_password = data['sudo_password']
webhook = data['webhook']
hook = Webhook(webhook)
embed = Embed(
    description='',
    color=16749644
    )
embed.add_field(name=message,  value='All Good Now')

while True:
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    command = 'sudo systemctl start application.service'
    a  = os.popen('systemctl status application.service').readlines()
    a = str(a)
    match = re.search(r'\b(running)\b',a)
    if match:
        time.sleep(3)
    else:
        print ("Faild at " + current_time)
        hook.send('ALERT :exclamation: ', embed=embed)
        p = os.system('echo %s|sudo -S %s' % (sudo_password, command))
