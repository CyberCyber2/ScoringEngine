#!/usr/bin/env python3
#TESTING SCRIPT TO GENERATE SCOREBOT DATA FROM A CLIENT. NOT FOR ACTUAL SCORING PURPOSES
import os
import sys
import time
import subprocess
import requests
import ssl
import random
#################################
SERVER="localhost:443" #bridged IP address
#headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
#data = '{"text":"Hello, World!"}'
#response = requests.post('https://localhost', headers=headers, data=data, verify=False)
#################################

possible_users = ["Cody", "Shrader", "Brehm"]
data = None
randSCR = None
randUSR = None
key = "cool"
for x in range(1,100):
    randUSR = random.randint(0,2)
    randSCR = random.randint(-1,4)
    data = str(possible_users[randUSR]) + ":" + str(randSCR + random.randint(-2,3)) + ":" + str(int((time.time() / 60))) + ":" + str(key) 
    os.system("curl -X POST -d " + data + " http://" + SERVER) 
    time.sleep(5)
