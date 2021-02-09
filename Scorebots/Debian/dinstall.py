#!/usr/bin/env python3
import os
import sys
import time
import subprocess
######Auto setup#######
mainUser = 'cyber' #the place to install ScoringEngine
if not os.path.isfile('''/home/''' + mainUser + '''/Desktop/ScoringEngine.py'''):
#the if loop makes it so that it doesn't run again once obfuscated(could also put into tmp file and replace orig)
	os.system('''apt install -y net-tools  >> /dev/null''')
	os.system(''' apt -y install python3-pip > /dev/null ''')
	os.system('''ps -ef | grep '[S]coringEngine.py' | grep -v grep | awk '{print $2}' | xargs -r kill -9''')
	os.system('''apt -y install htop >> /dev/null && apt install -y curl''')
	#os.system('''python3 -m pip install python-tk > /dev/null''')
	os.system('''python3 -m pip pip install numpy > /dev/null''')
	os.system('''pip3 install --upgrade setuptools > /dev/null''')
	os.system('''pkill -f ScoringEngine.py ; nohup python3 /home/cyber/Desktop/ScoringEngine.py &''')					
	os.system('''sudo apt-get -y install python3-matplotlib >> /dev/null''' )
	os.system('''pip install numpy scipy > /dev/null''')
	os.system('''apt-get -y install git  > /dev/null''')
	os.system('''apt install -y python3-venv python3-pip python3-tk > /dev/null''')
	os.system('''rm -rf /home/''' + mainUser + '''/Desktop/TeamInfo1.py''')
	#os.system('''touch TeamInfo1.py /home/''' + mainUser + '''/Desktop''')
	os.system('''sudo date -s "$(wget -qSO- --max-redirect=0 google.com 2>&1 | grep Date: | cut -d' ' -f5-8)Z" > /dev/null ''')
	#os.system('''wget https://raw.githubusercontent.com/CyberCyber2/LinuxScorebot/main/TeamInfo.py -q -O - > TeamInfo1.py''')
	os.system('''wget https://raw.githubusercontent.com/CyberCyber2/LinuxScorebot/main/Scorebots/DebianR3 -q -O - > scorebot.py''')
	os.system('''git clone https://github.com/chris-rands/emojify;''')
	os.system('''cd /home/''' + mainUser + '''/Desktop/emojify  >> /dev/null && ./emojify --input /home/''' + mainUser +'''/Desktop/scorebot.py --output /home/''' + mainUser + '''/Desktop/ScoringEngine.py >> /dev/null''')
	#os.system('''cd /home/''' + mainUser + '''/Desktop/emojify  >> /dev/null && ./emojify --input /home/''' + mainUser +'''/Desktop/TeamInfo1.py --output /home/''' + mainUser + '''/Desktop/TeamInfo.py >> /dev/null''')
	os.system('''rm -rf /home/''' + mainUser + '''/Desktop/install.py && rm -rf /home/''' + mainUser + '''/Desktop/scorebot.py && rm -rf /home/''' + mainUser + '''/Desktop/emojify ''')

	inputVar = str(input("Would you like to start the scorebot? [y/n]"))
	yesCheck = "y"
	if inputVar == yesCheck:
		os.system('''echo [[[Starting Scorebot]]]''')
		os.system('''cd /home/''' + mainUser + '''/Desktop/ && chmod 777 ScoringEngine.py && nohup python3 ScoringEngine.py > /dev/null 2>&1 &''')
	else:
		sys.exit()
