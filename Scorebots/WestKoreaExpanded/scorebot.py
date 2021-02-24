#!/usr/bin/env python3
import os
import sys
import time
import pwd
import grp
import subprocess
######################
mainUser = 'jongun5' #the place to install ScoringEngine
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
users = [User(mainUser), User('jongun5'), User('aang'), User('barackobama'),User('vladimirputin'), User('xijinping'),User('sokka'),User('zuko'), User('jwest'), User('ballen') ] #If a user is deleted, you get a penalty
services = [Service('cupsd', 631)] #If a service is down, you get a penalty
allTasks = [
	
	Task('Beginner','Beginner Forensics 1', 5, '[ "$(grep 2.4.18 /home/'+ mainUser + '/Desktop/Beginner/BForensics1)" ]'),
	Task('Beginner','Beginner Forensics 2', 5, '[ "$(grep \'/etc/opt/CoolGuyJoe.txt\' /home/'+ mainUser + '/Desktop/Beginner/BForensics2)" ]'),
	Task('Beginner','Beginner Forensics 3', 5, '[ "$(grep 1065281 /home/'+ mainUser + '/Desktop/Beginner/BForensics3)" ]'),
	Task('Beginner','Beginner Forensics 4', 5, '[ "$(grep -- \'-r-Srw--wt\' /home/'+ mainUser + '/Desktop/Beginner/BForensics4" ]'),
	Task('Returner', 'Returner Forensics 1', 5, '[ "$(grep 6f261657-4d6c-44ff-9bf4-1ea86832932c /home/'+ mainUser + '/Desktop/Returner/RForensics1)" ]'), 
	Task('Returner','Returner Forensics 2', 5, '[ "$(grep 2740 /home/'+ mainUser + '/Desktop/Returner/RForensics2)" ]'), 
	Task('Returner','Returner Forensics 3', 5, '[ "$(grep 2048 /home/'+ mainUser + '/Desktop/Returner/RForensics3)" ]'), 
	Task('Returner','Returner Forensics 4', 5, '[ "$(grep 48 /home/'+ mainUser + '/Desktop/Returner/RForensics4)" ]'), 
	Task('Returner','Returner Forensics 5', 5, '[ "$(grep \'oh, you like "Your Name"? how about you name every name then. checkmate.\' /home/'+ mainUser + '/Desktop/Returner/RForensics5Steganography.png)" ]'),
	Task('Advanced', 'Advanced Forensics 1', 3, ' ! [ "$(lsattr /home/'+ mainUser + '/Desktop/Advanced/AForensics1\:Diary | grep -- -i)" ]' ),
	Task('Advanced', 'Advanced Forensics 2', 3, ' [ "$(grep RecursiveUnzipIsCool /home/'+ mainUser + '/Desktop/Returner/AForensics2)" ]' ),
	Task('Advanced', 'Advanced Forensics 3', 3, ' [ "$(grep DCQ7_c14 /home/'+ mainUser + '/Desktop/Returner/AForensics3)" ]' ),
	Task('Advanced', 'Advanced Forensics 5', 3, ' [ "$(grep BeansBufferOverflow2 /home/'+ mainUser + '/Desktop/Returner/AForensics5)" ]' ),
	#####
	Task('Beginner','removed Sokka as admin', 1, '! [ "$(grep jongun5,vladimirputin,sokka /etc/group)" ]'),  
	Task('Beginner','installed stellarium', 3, ' [ "$(dpkg-query -l stellarium | grep no)" ]'), ; do apt-get remove --purge stellarium;apt-get clean; apt-get autoremove to refresh
	Task('Beginner','ballen has a password', 2, ' ! [ "$(passwd --s ballen | awk \'{ print $2 }\' | grep L || passwd --s ballen | awk \'{ print $2 }\' | grep NP)" ] '),  
	Task('Beginner','removed hidden desktop malware', 2, ' ! [ "$(find /home/jongun5/Desktop/.Mal*)" ] '),  
	Task('Beginner','removed crontab startup script', 2, ' ! [ "$(grep touch /var/spool/cron/crontabs/root)" ] '),  
	Task('Beginner','removed user21', 1, '! [ "$(grep user21  /etc/passwd)" ]'), 
	Task('Beginner','Added user DengXiaoping12', 2, ' [ "$(grep DengXiaoping12  /etc/passwd)" ]'),
	Task('Beginner','removed user23', 1, '! [ "$(grep user23  /etc/passwd)" ]'), 
	Task('Beginner','ufw started', 1, '[ "$(ufw status | grep -w active)" ] '),  
	Task('Beginner','Malicious UFW rule removed', 2, ' ! [ "$(grep \'allow tcp 13213 0.0.0.0/0 any 0.0.0.0/0 in\' /etc/ufw/user.rules)" ] '),  
	Task('Beginner','toor account removed', 2, '! [ "$(grep toor /etc/passwd)" ]'), 
	Task('Beginner','shadow correct file permissions set', 3, '[ "$(stat -c "%a %n" /etc/shadow | grep 640)" ]'),  
	Task('Beginner','telnet removed', 2, ' [ "$(dpkg-query -l telnet | grep un)" ]'),  
	#Task('Beginner','netcat backdoor removed', 2, '! [ "$(pgrep nc | grep 84837)" ]'), #
	#Task('Returner','netcat backdoor removed', 2, '! [ "$(netstat -tulpn | grep netcat)" ]'),
	Task('Returner','netcat backdoor removed', 2, '! [ "$(ls /etc/init.d | grep myCoolScript)" ]'),
	Task('Advanced','Malicious systemD unit file removed', 5, ' ! [ "$(find /lib/systemd/system/HA*)" ] '),  
	Task('Beginner','disabled guest user', 2, ' [ "$(grep false /etc/lightdm/lightdm.conf)" ] '),  
	Task('Beginner','login.defs Login_retries fixed', 2, '! [ "$(grep 5000000000000000000000000 /etc/login.defs)" ] '),  
	Task('Beginner','login.defs Password max days fixed', 2, '! [ "$(grep 99999 /etc/login.defs)" ] '),
	Task('Beginner','sshd_config Port set', 2, ' ! [ "$(grep \'Port 2222\' /etc/ssh/sshd_config)" ] '),  
	Task('Beginner','sshd_config Protocol set', 2, '[ "$(grep \'Protocol 2\' /etc/ssh/sshd_config)" ]'),  
	Task('Beginner','root login requires a password', 4, '[ "$(grep \'$USER ALL=(ALL) NOPASSWD: ALL\' /etc/sudoers)" ]'),
	Task('Advanced','SSH key pair created', 5 , '[ "$(ls -a /root/.ssh/ | grep rsa" ]'),
	Task('Returner','ExecShield prevents against buffer overflows', 5,' [ "$(grep kernel.exec-shield /etc/sysctl.conf)" ] '),  
	Task('Returner','ASLR randomization enabled', 5,' [ "$(grep kernel.randomize_va_space /etc/sysctl.conf)" ] '),  
	Task('Returner', 'IPv6 is disabled', 3,'[ "$(grep net.ipv6.conf.all.disable_ipv6 /etc/sysctl.conf | grep 1)" ]'),
	Task('Returner','Martian packets are logged ', 3,' [ "$(grep net.ipv4.conf.all.log_martians /etc/sysctl.conf | grep 1)" ] '),  
	Task('Returner','SYN cookies are enabled', 3,' [ "$(grep net.ipv4.tcp_syncookie /etc/sysctl.conf | grep 1)" ] '),  
	Task('Returner','Spoofing protection enabled', 3,'[ "$(grep net.ipv4.conf.all.rp_filter /etc/sysctl.conf | grep 1 )" ]'),  
	Task('Returner','Dangerous banner removed ', 1,'! [ "$(grep funny /etc/issue.net)" ] '),  
	Task('Returner','Malicious command alias removed ', 1,'! [ "$(grep HAHA* /root/.bashrc)" ] '),
	Task('Beginner','Media files removed', 1, ' ! [ "$(find /home/barackobama/ | grep mp3)" ]'),  
	Task('Beginner','Secure hashing algorithm is used', 1,'[ "$(grep ENCRYPT_METHOD\ SHA512 pas/etc/login.defs)" ]'),  
	Task('Beginner','Failed logins are logged', 1,'[ "$(grep FAILLOG_ENAB /etc/login.defs | grep yes)" ]'),  
	Task('Returner','Bad Hostname Changed', 2,' ! [ "$(hostnamectl | grep HackedByEastKorea)" ]'),
	Task('Advanced', 'chattr immutable permission removed', 3, ' ! [ "$(lsattr /home/'+ mainUser + '/Desktop/Advanced/AForensics1\:Diary | grep -- -i)" ]' ),
	#Task('Advanced','Sticky Bit set on TMP', 3,'[ "$(stat -c \'%a\' /tmp | grep 1777)" ]'),
	#Task('Advanced','SUID bit set on /usr/bin/sudo', 3,'[ "$(stat -c \'%a\' /usr/bin/sudo | grep 4755)" ]'), #Removing the SUID bit broke my image, I had to go to recovery mode and reset it. 
	Task('Returner','Fork Bomb protection added', 3,' ! [ "$(grep -o nproc /etc/security/limits.conf | wc -l | grep 1)" ]'),
	Task('Advanced','Core dumps restricted', 3,' [ "$(grep \'hard core\' /etc/security/limits.conf)" ]'),
	Task('Beginner','WorldLeaders Group created', 2,' [ "$(grep WorldLeaders /home/etc/groups)" ]'),
	Task('Advanced','NoExec kernel parameter set for buffer overflows', 4,' [ "$(dmesg | grep NX | grep active)" ]'),
	Task('Returner','Malicous domain redirections removed', 3,' ! [ "$(grep google /etc/hosts)" ]'),
	Task('Returner','Fail2ban installed', 3, ' [ "$(systemctl list-units --type=service | grep fail2ban)" ]'), 
	Task('Returner','Apache2 Sensitive information hidden', 3, ' [ "$(grep ServerSignature /etc/apache2/apache2.conf)" ]'),  #There are more things, but too lazy to score 
	Task('Returner','Apache2 mod security WAF installed', 3, ' [ "$(dpkg-query -l libapache2-modsecurity2)" ]'),
	Task('Returner','Apache2 mod invasive installed', 3, ' [ "$(dpkg-query -l libapache2-mod-evasive)" ]'), 
	Task('Returner','Mysql bind address set', 2,'[ "$(grep 127.0.0.1 /etc/mysql/mysql.conf.d/mysqld.cnf)" ]'),
	Task('Returner','Mysql correct port set', 2,'[ "$(grep 3306 /etc/mysql/mysql.conf.d/mysqld.cnf)" ]'),
	Task('Returner','Mysql local infile disabled', 2,'[ "$(grep local-infile=0 /etc/mysql/mysql.conf.d/mysqld.cnf)" ]'),
	Task('Returner','PHP basic information hidden', 2,'[ "$(grep expose_php /etc/mysql/mysql.conf.d/mysqld.cnf | grep -i off)" ]'), 
	Task('Returner','PHP dangerous functions are blocked', 2,'[ "$(grep popen /etc/php/7.0/cli/php.ini)" ]'), #There are more things, but too lazy to score 
	Task('Returner','PHP remote code execution blocked', 2,'[ "$(grep fopen /etc/php/7.0/cli/php.ini | grep -i off)" ]'),
	Task('Returner','PHP file uploads enabled', 2,'[ "$(grep file_uploads /etc/php/7.0/cli/php.ini | grep -i on)" ]'),
	Task('Returner','PHP dangerously large file upload size fixed', 4,' ! [ "$(grep upload_max_filesize /etc/php/7.0/cli/php.ini | grep -i Gb)" ]'),
	Task('Returner','PHP max execution time reduced', 3,' ! [ "$(grep max_execution /etc/php/7.0/cli/php.ini | grep 5000)" ]'),
	Task('Returner','PHP Open Base Dir set', 3,' ! [ "$(grep open_basedir /etc/php/7.0/cli/php.ini | grep \';\')" ]'),
	Task('Returner','Password file in hidden directory removed', 3,'! [ "$(ls -al \'/home/jongun5/.. \' | grep password)" ] '),
	Task('Beginner','Mahjongg game removed', 3, ' ! [ "$(ls /home/'+ mainUser + '/Desktop | grep mahjongg)" ]'),
	Task('Beginner','Langauge changed back to english', 1, ' ! [ "$(locale | grep ae_EG)" ]'),
	Task('Advanced','File ACL created according to scenario', 3, ' [ "$(grep -- -rwxrw-rw-+ home/'+ mainUser + '/Desktop/SecretMilitaryPlans/NuclearCodes.conf)" ]'),
	Task('Returner','LUKS setup on /dev/sdb1', 5,' [ "$(lsblk | grep luks)" ] '),
	Task('Returner','Partition /dev/sdb2 created', 5,' [ "$(lsblk | grep sdb2)" ] '), #mount it correctly in fstab or you will need to go into recovery mode and reverse it
	Task('Beginner', 'Configure security updates to be downloaded and installed immediately', 3, ' [ "$(grep Unattended-Upgrade /etc/apt/apt.conf.d/10periodic | grep 0)" ] '), ###DOES THIS WORK>>>>
	Task('Beginner','PAM Password complexity set', 5,' [ "$(grep "ucredit=‐1 lcredit=‐1 dcredit=‐1 ocredit=‐1" /etc/pam.d/common‐password )" ] '),
	Task('Beginner','System checks for updates daily', 2, '[ "$(grep APT::Periodic::Update-Package-Lists /etc/apt/apt.conf.d/10periodic | grep 1 )" ]'),
	Task('Beginner','Configure Ubuntu software to be downloaded from main, universe, restricted and multiverse repositories',5, '[ "$(grep http://archive.ubuntu.com/ubuntu /etc/apt/sources.list)" ]'),
	Task('Returner','Samba password file removed', 2, '! [ "$(ls /home/samba/sambashare | grep passwords)" ]'),
	Task('Returner','Samba unauthorized user removed', 2, '! [ "$(grep sokka /etc/samba/smb.conf)" ]'),
	Task('Returner','Samba ethernet links allowed', 2, ' [ "$(cat /etc/samba/smb.conf | grep eth | grep \*)" ]'),
	Task('Returner','Samba anonymous accounts disabled', 2, ' [ "$(grep \'restrict anonymous\' /etc/samba/smb.conf)" ]'),
	Task('Returner','Samba insecure SMB protocol version disabled', 2, ' ! [ "$(grep SMB1 /etc/samba/smb.conf)" ]'),
	Task('Advanced','SELinux mode set to permissive', 3, ' [ grep -o permissive /etc/selinux/config)" ]'),
	Task('Returner','VSFTPD blocks anonymous logins', 3, ' [ grep -o anonymous /etc/vsftpd.conf | grep -o no" ]'),
	Task('Returner','VSFTPD blocks unauthorized users', 3, ' [ grep denied_users /etc/vsftpd.conf || grep allowed_users /etc/vsftpd.conf ]'),
	Task('Returner','VSFTPD enables SSL/TLS connections', 3, ' [ grep ssl_enable /etc/vsftpd.conf | grep -o yes" ]'),
	Task('Returner','VSFTPD uses SSLv3', 3, ' [ grep sslv3 /etc/vsftpd.conf | grep -o yes" ]'),
	Task('Returner','VSFTPD listening on correct port', 3, ' [ grep 990 /etc/vsftpd.conf || grep 21 /etc/vsftpd.conf ]'),
	Task('Returner','Firefox prompts user to remember paswords', 3, ' [ grep signon.rememberSignons /home/'+ mainUser + '/.mozilla/firefox/cf9mjv6f.default/prefs.js]'),
	Task('Returner','Firefox blocks popups', 3, ' [ grep dom.disable_open_during_load /home/'+ mainUser + '/.mozilla/firefox/cf9mjv6f.default/prefs.js]'),
	Task('Returner','Firefox blocks dangerous and deceptive content', 3, ' [ grep browser.safebrowsing.malware.enabled /home/'+ mainUser + '/.mozilla/firefox/cf9mjv6f.default/prefs.js || grep browser.safebrowsing.phishing.enabled /home/'+ mainUser + '/.mozilla/firefox/cf9mjv6f.default/prefs.js ]'),
	Task('Advanced','Firefox HSTS file reinstated', 3, ' [ grep signon.rememberSignons /home/'+ mainUser + '/.mozilla/firefox/cf9mjv6f.default/prefs.js]'),
	Task('Returner','redis package updated to prevent DoS attacks', 3, '  [ dpkg --list | grep redis | grep 3.0.6 ]'),
	Task('Returner','redis package requires passwords', 3, ' [grep \"requirepass \"| grep \"#" ]'),
	Task('Advanced','Drovorub malware mitigated by disabling un-needed kernel modules', 3, ' [sysctl kernel.modules_disabled | grep 1 ]'),
	Task('Advanced','Time check time of use race conditions via hardlinks fixed', 3, ' [grep 1 /proc/sys/fs/protected_hardlinks]'),
	Task('Advanced','Time check time of use race conditions via symlinks fixed', 3, ' [grep 1 /proc/sys/fs/protected_symlinks]'),
	#FIX#Task('Advanced','Rare, deprecated protocol DecNet is blocked', 3, ' [grep net-pf-12 /etc/modprobe.d/blacklist-rare-network.conf | grep off ]'),
	Task('Advanced','More secure ptrace options enabled', 3, ' [grep 0 /proc/sys/kernel/yama/ptrace_scope || grep 0 /etc/sysctl.d/10-ptrace.conf]'), 
	Task('Advanced','Microdata sampling enabled to prevent vulnerabilities ', 3, ' [grep mds=off /etc/default/grub]'),
	#Task('Advanced','L1 terminal fault mitigated', 3, ' ! [grep on /sys/devices/system/cpu/smt/control]'), #Only works on certain CPUs
	Task('Advanced','iTLB errors fixed ', 3, ' [grep nx_huge_pages= /etc/default/grub]'),
	Task('Returner','User Quotas enabled', 3, ' [grep usrquota /etc/fstab]'),
	Task('Advanced','Apt backdoor removed', 2, '! [ "$(grep netcat /etc/apt/apt.conf.d/42filesystem)" ]'), #check if file deleted too
	Task('Advanced','XiJinping bashrc backdoor removed', 2, '! [ "$(grep TMPNAME2 /home/xijinping/.bashrc)" ]'),
	Task('Advanced','Linux driver backdoor removed', 2, '! [ "$(grep SUBSYSTEM /etc/udev/rules.d/71-vbox-kernel-drivers.rules)" ]'),
	Task('Advanced','Sudoers cve-2019-14287 mitigated ', 2, '! [ "$(grep aang /etc/sudoers)" ]')
 
	####TO Add#####
	#set the right permission, 700 for ~/.ssh and 600 for authorized_keys: backdoor
	#update the kernel
	#dirty cow: fix by mitigating or upgrading kernel?
	#more services to update
	#add more beginner and returner vulnerabilities
	#add web ex(already added, just check and finish the website)
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
	h = open('/home/jongun5/Desktop/ScoreReport.html','w')
	h.write('<!DOCTYPE html> <html> <head> <meta name="viewport" content="width=device-width, initial-scale=1"> <style> * { box-sizing: border-box; } .column { float: left; padding: 10px; height: 1500px; } .left, .right { width: 25%; } .middle { width: 50%; } .row:after { content: ""; display: table; clear: both; }</style> </head> <body><div class="row"> <div class="column left" style="background-color:#0d60bf;"></div> <div class="row"> <div class="column middle" style="background-color:#fff;"><h1 style="text-align: center;"><span style="font-family: arial, helvetica, sans-serif;">Score Report</span></h1><h2 style="text-align: center;"><br /><span style="font-family: arial, helvetica, sans-serif;">' + percent + ' completed</span></h2><p> </p>')
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
                        + ' is NOT functional: - 5 points</span></p>')
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

	h.write('</div> <div class="row"> <div class="column right" style="background-color:#0d60bf;"></div> </body>')
	h.write('<meta http-equiv="refresh" content="20">')
	h.write('<footer><h6>Cyber Club</h6></footer>')

'''
def notify(ls,cs):
	#Creates a popup on the screen
	icon_path = "/usr/bin/scorebot/scoring.png"
	if (cs > ls):
		os.system('notify-send -i /home/'+ mainUser + icon_path + '\'You Earned Points!\' ')

	if (cs < ls):
		os.system('notify-send -i /home/'+ mainUser + icon_path + '\'You Lost Points!\' ')
'''
######################

while True:
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
	#lastPoints = currentPoints
	currentPoints = currentPoints - penalties
	update()
	#notify(lastPoints,currentPoints)
	time.sleep(5) #time between score checks
