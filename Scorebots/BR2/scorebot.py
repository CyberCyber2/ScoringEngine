#!/usr/bin/env python3
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
######################
mainUser = 'cyber' #the place to install ScoringEngine
today = _datetime.date.today()
######################
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
			#os.system('''netstat -tulpn | grep ''' + str(self.getPort())) + ' > /dev/null'  == 0:
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
######################
users = [User(mainUser), User('sokka'),  User('aang'),  User('zuko'), User('vladimir'), User('sokka'),User('jongun'),User('jinping') ] #If a user is deleted, you get a penalty
services = [] #If a service is down, you get a penalty
allTasks = [
	Task('Beginner','Beginner Forensics 1', 5, '[ "$(grep /var/spool/anacron/88888.txt /home/'+ mainUser + '/Desktop/Forensics1)" ]'), #
	Task('Beginner','Returner Forensics 2', 5, '[ "$(grep 39944190 /home/'+ mainUser + '/Desktop/Forensics2)" ]'), #
	Task('Beginner','Beginner Forensics 3', 5, '[ "$(grep steganographyiscool /home/'+ mainUser + '/Desktop/Forensics3)" ]'),  #
	#######
	Task('Beginner','Removed Unauthorized user vladimir', 1, ' [ ! "$(grep vladimir /etc/passwd)" ]'), 
	Task('Beginner','firewall enabled', 1, ' [ ! "$(ufw status | grep inactive)" ]'), 
	Task('Beginner','Removed Unauthorized user Haxor', 1, ' [ ! "$(grep Haxor /etc/passwd)" ]'), 
	Task('Beginner','Removed Unauthorized HIDDEN user toor', 3, ' [ ! "$(grep toor /etc/passwd)" ]'), 
	Task('Beginner','Removed Unauthorized admin sokka', 1, ' [ ! "$(grep sudo /etc/group | grep sokka)" ]'),
	Task('Beginner','Added user Joeseph', 1, ' [  "$(grep joeseph /etc/passwd)" ]'), 
	Task('Beginner','Added group worldleaders', 1, ' [  "$(grep wordleaders /etc/group)" ]'), 
	Task('Beginner','sokka has a password', 2, ' [  "$(grep \'\$*\$\' /etc/shadow | grep sokka)" ]'),
	Task('Beginner','Cyber has a more secure password', 2, ' ! [  "$(cat /etc/shadow | grep Rgnod | grep \'\$\' )" ]'),  
	Task('Beginner','Added group worldleaders', 1, ' [  "$(grep wordleaders /etc/group)" ]'), 
	Task('Beginner','Unauthorized malware netcat removed', 2, ' [ ! "$(dpkg --list | grep netcat)" ]'), 
	Task('Beginner','Unauthorized malware john removed', 2, ' [ ! "$(dpkg --list | grep john)" ]'), 
	Task('Beginner','Unauthorized malware hydra removed', 2, ' [ ! "$(dpkg --list | grep hydra)" ]'), 
	Task('Beginner','Unecessary service vsftpd removed', 1, ' [ ! "$(dpkg --list | grep vsftpd)" ]'), 
	Task('Beginner','Stellarium Installed', 2, ' [  "$(dpkg --list | grep stellarium)" ]'), 
	#Task('Beginner','', 2, ' [  "$()" ]'), 
	Task('Beginner','Correct permissions set on /etc/passwd', 2, ' [ ! "$(stat -c "\%a \%n" /etc/passwd | grep 777)" ]'), #
	Task('Beginner','Media Files removed', 2, ' [ ! "$(ls /home/jongun/Pictures | grep jp)" ]'),
	Task('Beginner','Hidden Desktop file removed', 2, ' [ ! "$(ls -al /home/cyber/Desktop | grep Virus)" ]'),
	Task('Beginner','Firewall rule added', 4, ' [ "$(grep 21 /etc/ufw/user.rules)" ]'), 
	Task('Beginner','netcat backdoor removed', 5, ' [ ! "$(grep netcat /var/spool/cron/crontabs/root)" ]'), 
	Task('Beginner','netcat service stopped', 3, ' [ ! "$(netstat -tulpn | grep netcat)" ]'), 
	Task('Beginner','added users to WorldLeaders group', 2, ' [  "$(grep worldleaders /etc/group | grep jinping)" ]'), 
	Task('Beginner','Firefox blocks dangerous and deceptive content', 3, ' ! [ "$(grep browser.safebrowsing.malware.enabled /home/'+ mainUser + '/.mozilla/firefox/79irpra1.default/prefs.js)" ]'),
	Task('Beginner','root login requires a password', 4, '! [ "$(grep NOPASSWD /etc/sudoers)" ]'),
	Task('Beginner','disabled guest user', 2, ' [ "$(grep false /etc/lightdm/lightdm.conf)" ] '), 
	Task('Beginner','bad alias removed', 3, ' [ ! "$(grep HAHA ~/.bashrc)" ] '), 
	Task('Beginner','Bad banner removed', 2, ' [ ! "$(grep "hacked" /etc/issue.net)" ]'),
	Task('Beginner','bad hostname fixed', 2, ' [ ! "$(grep HACKED /etc/hostname)" ] '), 
	Task('Beginner','login.defs Password max days fixed', 2, '! [ "$(grep 899999 /etc/login.defs)" ] '),
	Task('Beginner','login.defs Password min days fixed', 2, '! [ "$(grep 100000 /etc/login.defs)" ] '),
	Task('Beginner','PAM Password complexity set', 5,' [ "$(grep ucredit=‐1 /etc/pam.d/common-password)" ] '),
	#updates
	Task('Beginner','System checks for updates daily', 5, ' [  "$(grep APT::Periodic::Update-Package-Lists /etc/apt/apt.conf.d/10periodic | grep 1)" ]'),
	Task('Beginner','System notifies updates immediately ', 5, ' [  "$(grep Unattended-Upgrade /etc/apt/apt.conf.d/10periodic | grep 0)" ]'),
	Task('Beginner','System downloads updates from MAIN server', 5, ' [  "$(grep http://archive.ubuntu.com/ubuntu /etc/apt/sources.list)" ]'),

	#openssh
	Task('Beginner','SSHD root login not permitted', 1, ' [ "$(grep PermitRoot /etc/ssh/sshd_config | grep no)" ]'),
	Task('Beginner','SSHD correct protocol set', 1, ' [ "$(grep Protocol /etc/ssh/sshd_config | grep 2)" ]'),
	Task('Beginner','SSHD uses port 2222', 1, ' [ "$(grep 2222 /etc/ssh/sshd_config)" ]'),    
	Task('SSHD X11 forwarding disabled','', 1, ' [ "$(grep X11Forwarding /etc/ssh/sshd_config | grep no)" ]'),  

	#samba
	Task('Beginner','Samba user cannot be logged into', 3, ' [  "$(grep samba /etc/passwd | grep login)" ]'),
	Task('Beginner','Removed Unauthorized samba share WorldDomination', 4, ' [ ! "$(grep WorldDomination /etc/samba/smb.conf )" ]'), 
	Task('Beginner','Removed Unauthorized user access to samba via sambapeople group', 2, ' [ ! "$(grep sambapeople /etc/group | grep sokka)" ]'), 
	Task('Beginner','Samba sambapeople share NOT writable', 4, ' [  "$(grep -A4  sambapeople /etc/samba/smb.conf | grep writable | grep no)" ]'), 
]
groups = [] #groups that must exist, or else a penalty

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


def notify(ph):
	#Creates a popup on the screen
	icon_path = "/usr/bin/scorebot/scoring.png"
	if (ph[-1] > ph[-2]):
		os.system('notify-send -i ' + icon_path + ' \'You Earned Points!\' ')

	if (ph[-1] < ph[-2]):
		os.system('notify-send -i ' + icon_path + ' \'You Lost Points!\' ')
####################################

pointHistory = [0,0,0] #list containing the history of points
HasEnteredTeamInfo = False
dUSR = ""
dMode = ""
dServIP = ""
key = "cool"
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

	####Create Graph#####
	Y = np.array(pointHistory) 
	ax = plt.axes()
	ax.plot(Y, linewidth=4, color="red")
	plt.axhline(y=0, color="black")
	ax.yaxis.set_major_locator(MaxNLocator(integer=True))
	plt.savefig('.graph.png',bbox='tight')
	update()
	time.sleep(20)
	#show()
