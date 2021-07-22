#!/usr/bin/env python3
import os
import sys
import time
import subprocess
import requests
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
mainUser = 'server' #the place to install ScoringEngine
injectSLA = requests.get('https://raw.githubusercontent.com/CyberCyber2/ScoringEngine/main/BaseFiles/ServerInjectSLA.py')
serverLoc = requests.get('https://raw.githubusercontent.com/CyberCyber2/ScoringEngine/main/BaseFiles/Server.py')
injectsConfLoc = requests.get('https://raw.githubusercontent.com/CyberCyber2/ScoringEngine/main/BaseFiles/ServerGrapher.py')
serverGrapherLoc= requests.get('https://raw.githubusercontent.com/CyberCyber2/ScoringEngine/main/BaseFiles/ServerGrapher.py')
with open ('ServerInjectSLA.py', 'w') as outf:
    outf.write(injectSLA.text)

with open ('Server.py', 'w') as outf:
    outf.write(serverLoc.text)

with open ('Injects.cnf', 'w') as outf:
    outf.write(injectsConfLoc.text)

with open ('ServerGrapher.py', 'w') as outf:
    outf.write(serverGrapherLoc.text)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
subprocess.call(["apt-get", "-qq", "-y" , "--ignore-missing", "install", "net-tools", "python3-pip", "curl", "python3-matplotlib", "git", "python3-venv", "python3-pip", "python3-tk" ])
os.system('python3 -m pip pip install numpy')
os.system('pip3 install --upgrade setuptools')
os.system('pip install numpy scipy matplotlib')
