#!/usr/bin/env python3
import os
import sys
import time
import subprocess
import requests
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
mainUser = 'cyber' #the place to install ScoringEngine
scoreBotLoc = requests.get('https://raw.githubusercontent.com/CyberCyber2/ScoringEngine/main/Scorebots/Testing.py')
teamInfoLoc = requests.get('https://raw.githubusercontent.com/CyberCyber2/LinuxScorebot/main/BaseFiles/TeamInfo.py')
with open ('TeamInfo1.py', 'w') as outf:
    outf.write(teamInfoLoc.text)

with open ('scorebot.py', 'w') as outf:
    outf.write(scoreBotLoc.text)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if not os.path.isfile('/home/' + mainUser + '/Desktop/ScoringEngine.py'): #If ScoringEngine.py doesn't already exist
    #Clean Up Previous Installations#
    print(f"{bcolors.WARNING}Info: Cleaning Previous Installations{bcolors.ENDC}")
    subprocess.call(["pkill", "-f", "ScoringEngine.py"])
    subprocess.call(["rm", "-rf", "/etc/scorebot"])

    print(f"{bcolors.WARNING}Info: Installing Needed Packages{bcolors.ENDC}")
    subprocess.call(["apt-get", "-qq", "-y" , "--ignore-missing", "install", "net-tools", "python3-pip", "curl", "python3-matplotlib", "git", "python3-venv", "python3-pip", "python3-tk" ])
    os.system('python3 -m pip pip install numpy')
    os.system('pip3 install --upgrade setuptools')
    os.system('pip install numpy scipy matplotlib')

    print(f"{bcolors.WARNING}Info: Starting Scoring Engine{bcolors.ENDC}")
    os.system('nohup python3 /home/a/Desktop/ScoringEngine.py &')                       
    os.system('date -s "$(wget -qSO- --max-redirect=0 google.com 2>&1 | grep Date: | cut -d' ' -f5-8)Z"')

    print(f"{bcolors.WARNING}Info: Obfuscating Scoring Engine{bcolors.ENDC}")
    os.system('git clone https://github.com/chris-rands/emojify;')
    os.system('cd /home/' + mainUser + '/Desktop/emojify  >> /dev/null && ./emojify --input /home/' + mainUser +'/Desktop/scorebot.py --output /home/' + mainUser + '/Desktop/ScoringEngine.py >> /dev/null')
    os.system('cd /home/' + mainUser + '/Desktop/emojify  >> /dev/null && ./emojify --input /home/' + mainUser +'/Desktop/TeamInfo1.py --output /home/' + mainUser + '/Desktop/TeamInfo.py >> /dev/null')
    subprocess.call(['chmod', "777", "/home/" + mainUser + "/Desktop/emojify"])
    
    print(f"{bcolors.WARNING}Info: Cleaning Up{bcolors.ENDC}")
    subprocess.call(["rm", "-rf", "/home/" + mainUser + "/Desktop/emojify"])
    subprocess.call(["rm", "-rf", "/home/" + mainUser + "/Desktop/TeamInfo1.py"])
    subprocess.call(["rm", "-rf", "/home/" + mainUser + "/Desktop/scorebot.py"])

    inputVar = str(input("Would you like to start the scorebot? [y/n]"))
    yesCheck = "y"
    if inputVar == yesCheck:
        print(f"{bcolors.WARNING}Info: STARTING SCOREBOT{bcolors.WARNING}")
        os.system('cd /home/' + mainUser + '/Desktop/ && chmod 777 ScoringEngine.py && nohup python3 ScoringEngine.py > /dev/null 2>&1 &')
    else:
        sys.exit()
