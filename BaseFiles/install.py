#!/usr/bin/env python3
import os
import sys
import time
import subprocess
import requests
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
mainUser = 'cyber' #the place to install ScoringEngine
scoreBotLoc = requests.get('https://raw.githubusercontent.com/CyberCyber2/ScoringEngine/main/BaseFiles/BaseScoreBot.py')
teamInfoLoc = requests.get('https://raw.githubusercontent.com/CyberCyber2/LinuxScorebot/main/BaseFiles/TeamInfo.py')
with open ('TeamInfo1.py', 'w') as outf:
    outf.write(teamInfoLoc.text)

with open ('scorebot.py', 'w') as outf:
    outf.write(scoreBotLoc.text)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if not os.path.isfile('''/home/''' + mainUser + '''/Desktop/ScoringEngine.py'''):
	#Clean Up Previous Installations#
	subprocess.call(["pkill", "-f", "ScoringEngine.py"])
	subprocess.call(["rm", "-rf", "/etc/scorebot"])

	subprocess.call(["apt-get", "-qq", "-y" , "--ignore-missing", "install", "net-tools", "python3-pip", "curl", "git", "python3-venv", "python3-pip", "python3-tk" ])
	os.system('''python3 -m pip pip install numpy''')
	os.system('''pip3 install --upgrade setuptools''')
	os.system('''pkill -f ScoringEngine.py ; nohup python3 /home/cyber/Desktop/ScoringEngine.py &''')					
	os.system('''sudo apt-get -y install python3-matplotlib >> /dev/null''' )
	os.system('''pip install numpy scipy matplotlib''')
	os.system('''date -s "$(wget -qSO- --max-redirect=0 google.com 2>&1 | grep Date: | cut -d' ' -f5-8)Z"''')
	os.system('''git clone https://github.com/chris-rands/emojify;''')
	os.system('''cd /home/''' + mainUser + '''/Desktop/emojify  >> /dev/null && ./emojify --input /home/''' + mainUser +'''/Desktop/scorebot.py --output /home/''' + mainUser + '''/Desktop/ScoringEngine.py >> /dev/null''')
	os.system('''cd /home/''' + mainUser + '''/Desktop/emojify  >> /dev/null && ./emojify --input /home/''' + mainUser +'''/Desktop/TeamInfo1.py --output /home/''' + mainUser + '''/Desktop/TeamInfo.py >> /dev/null''')
	subprocess.call(['chmod', "777", "/home/" + mainUser + "/Desktop/emojify"])
	#Delete not needed files#
	subprocess.call(["rm", "-rf", "/home/" + mainUser + "/Desktop/emojify"])
	subprocess.call(["rm", "-rf", "/home/" + mainUser + "/Desktop/TeamInfo1.py"])
	subprocess.call(["rm", "-rf", "/home/" + mainUser + "/Desktop/scorebot.py"])

	#subprocess.call([''])
	inputVar = str(input("Would you like to start the scorebot? [y/n]"))
	yesCheck = "y"
	if inputVar == yesCheck:
		os.system('''echo [[[Starting Scorebot]]]''')
		os.system('''cd /home/''' + mainUser + '''/Desktop/ && chmod 777 ScoringEngine.py && nohup python3 ScoringEngine.py > /dev/null 2>&1 &''')
	else:
		sys.exit()
