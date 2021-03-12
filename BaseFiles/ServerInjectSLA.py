import matplotlib.pyplot as plt 
import subprocess, platform, os
import hashlib
import urllib.request
import re
import time
from difflib import SequenceMatcher
import configparser
from configparser import *
import os.path
#import mysql.connector
from urllib.error import HTTPError, URLError
import logging
import socket
import paramiko
import ftplib
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#checkInterval=5
ftpFile = ""
ftpFileHash = ""
ftpPath = ""
ftpUSR = ""
ftpPWD = ""
serverFTPDir = ""
apacheCheck = ""
apacheWebsite = ""
dataDirectory = ""
mySQL_Query = "" 
smbUSR = ""
smbPWD = ""
smbSHR = ""
smbSHRFile = ""
sshUSR = ""
sshPWD = ""
sshPRT = ""
#####
injectSSHCurr = ""
injectSMBCurr = ""
injectApacheCurr = ""
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
class Team:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.ftpHIST = []
        self.internetHIST = []
        self.apacheHIST = []
        self.sambaHIST = []
        self.sshHIST = []
    def getName(self):
        return self.name
    def getAddress(self):
        return self.address
    def countUptime(self, service, currInject): 

        if service == "internet":
            if (checkInternet(self.address) == "Ok"):
                self.internetHIST.append("1")
                print("Internet reliable, added 1")
                print(self.internetHIST)
            else:
                self.internetHIST.append("0")
                print("Internet unreliable, added 0")
                print(self.internetHIST)
            internetReliability = str(self.internetHIST.count("1") + self.internetHIST.count("0") * (-5))
            return internetReliability

        if service == "ftp":
            if (checkFTP(str(self.getAddress()),"21",ftpFile, ftpFileHash, currInject) == "Ok"):
                self.ftpHIST.append("1")
                print("ftp reliable, added 1")
                print(self.ftpHIST)
            else:
                self.ftpHIST.append("0")
                print("ftp unreliable, added 0")
                print(self.ftpHIST)
            ftpReliability = str(self.ftpHIST.count("1") + self.ftpHIST.count("0") * (-5))
            return ftpReliability

        if service == "apache":
            print("Service is apache")
            if (check_apache2(str(self.getAddress()), currInject) == "Ok"):
                self.apacheHIST.append("1")
                print("apache2 reliable, added 1")
                print(self.apacheHIST)
            else:
                self.apacheHIST.append("0")
                print("apache2 unreliable, added 0")
                print(self.apacheHIST)
            apacheReliability = str(self.apacheHIST.count("1") + self.apacheHIST.count("0") * (-5))
            return apacheReliability

        if service == "samba":
            print("Service is samba")
            if (checkSMB(str(self.getAddress()) , str(self.getName()), currInject) == "Ok"):
                self.sambaHIST.append("1")
                print("samba reliable, added 1")
                print(self.sambaHIST)
            else:
                self.sambaHIST.append("0")
                print("samba unreliable, added 0")
                print(self.sambaHIST)
            sambaReliability = str(self.sambaHIST.count("1") + self.sambaHIST.count("0") * (-5))
            return sambaReliability

        if service == "ssh":
            print("Service is SSH")
            if (checkSSH(str(self.getAddress()), sshPRT, sshUSR, sshPWD, currInject) == "Ok"):
                self.sshHIST.append("1")
                print("ssh reliable, added 1")
                print(self.sshHIST)
            else:
                self.sshHIST.append("0")
                print("ssh unreliable, added 0")
                print(self.sshHIST)
            sshReliability = str(self.sshHIST.count("1") + self.sshHIST.count("0") * (-5))
            return sshReliability    

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
class CaseConfigParser(SafeConfigParser):
     def optionxform(self, optionstr):
         return optionstr
allTeams = [
    Team('Suriya', '192.168.1.244'),
    Team('Ahri', '192.168.1.245')
]
def similar(a, b): #Just incase the hash has an extra space, don't feel like removing space
    return SequenceMatcher(None, a, b).ratio()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def checkInternet(ip):
    hostname = ip
    response = os.system("ping -c 1 " + hostname)
    pingstatus = "Fail"
    if response == 0:
        pingstatus = "Ok"
    else:
        pingstatus = "Fail"
    return pingstatus

def checkFTP(ip, port, checkfile, filehash, currInject):
    if (currInject == "1"):
        ftpstatus = "Fail"
        try:
            print("FILE HASH: " + filehash)
            print("CHECK FILE:" + checkfile)
            print("ftpUSR:" + ftpUSR)
            print("ftpPWD" + ftpPWD)
            print("ftpPath:" + ftpPath)
            print("serverFTPDir:" + serverFTPDir)
            ftp = ftplib.FTP(ip) 
            ftp.login(ftpUSR, ftpPWD)
            ftp.cwd(ftpPath)
            ftp.retrbinary("RETR " + checkfile, open(checkfile, 'wb').write)
            f = "/home/" + serverFTPDir + "/Desktop/" + checkfile #FILE DOWNLOADED FROM CLIENT TO SERVER
            checkHash = os.popen(("sha1sum " + f + "| cut -d' ' -f1")).read()
            if (float(similar(checkHash,filehash)) >= 0.9):
                print("FTP hashes match")
                ftpstatus = "Ok"
            else:
                print("Client Hash: " + checkHash + " Server Hash: " + ftpFileHash)
                ftpstatus = "Fail"
            ftp.quit()
        except Exception as e:
            print("FTP hash exception: " + str(e) + " for " + str(ip))
            ftpstatus = "Fail"
        return (ftpstatus)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def checkSMB(ip, teamName, cI):

    if (int(cI) == 1):
        tempFileCheck = str(teamName) + ".txt" #tell them to add this file on client
        try:
            subprocess.call(['smbget', "smb://" + str(ip) + "/" + str(smbSHR) + "/" + str(tempFileCheck), "-U" , smbUSR + '%' + smbPWD])
            if not (os.path.isfile(str(tempFileCheck))):
                print("Error: could not get SMB file: " + str(tempFileCheck) + " from " + str(ip))
                return ("Fail")
            subprocess.call(['rm', '-rf', str(tempFileCheck)])
            return("Ok")
            print ("Deleted file: " +  str(tempFileCheck))
        except Exception as e:
            print("SMB ERROR: " + str(e))
            subprocess.call(['rm', '-rf', str(tempFileCheck)])
            return ("Fail")
    else:
        print("SMB ERROR: Inject ID not found for " + cI + " of type: " + str(type(cI)))

     if (int(cI) == 2):
        tempFileCheck = str(smbSHRFile) #tell them to add this file on client
        try:
            subprocess.call(['smbget', "smb://" + str(ip) + "/" + str(smbSHR) + "/" + str(tempFileCheck), "-U" , smbUSR + '%' + smbPWD])
            if not (os.path.isfile(str(tempFileCheck))):
                print("Error: could not get SMB file: " + str(tempFileCheck) + " from " + str(ip))
                return ("Fail")
            subprocess.call(['rm', '-rf', str(tempFileCheck)])
            return("Ok")
            print ("Deleted file: " +  str(tempFileCheck))
        except Exception as e:
            print("SMB ERROR: " + str(e))
            subprocess.call(['rm', '-rf', str(tempFileCheck)])
            return ("Fail")
    else:
        print("SMB ERROR: Inject ID not found for " + cI + " of type: " + str(type(cI)))
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def checkDNS(ip, recordType): pass
#dig google.com ANY +noall +answer
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def checkRDP(ip, port): pass
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def checkSSH(ip, port, usr, pwd, cI):
    try:
        if (int(cI) == 1):
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(str(ip), int(port), str(usr), str(pwd))
            stdin, stdout, stderr = ssh.exec_command("ls -l")
            lines = stdout.readlines()
            print (lines)
            return ("Ok")
        else:
            print("SSH ERROR: Inject ID not found for " + cI + " of type: " + str(type(cI)))
            return("Fail")
    except Exception as e:
        print("SSH ERROR: " + str(e))
        return ("Fail")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def checkVNC(ip, port): pass
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def checkSMTP(ip, port): pass
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def checkMYSQL(ip, port): pass
 #   mydb = mysql.connector.connect(host=str(ip), user=mySQL_USR, password=mySQL_PWD, database=mySQL_DB )
 #   mycursor = mydb.cursor()
 #   mycursor.execute(mySQL_Query) #SELECT name, address FROM customers
 #   myresult = mycursor.fetchall()
 #   for x in myresult:
        #check
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def check_apache2(ip, cI):
    if (int(cI) == 1):
        url = str ("http://" + ip + "/" + apacheWebsite)
        try:
            response = urllib.request.urlopen(url, timeout=5).read().decode('utf-8')
        except HTTPError as error:
            logging.error('Data not retrieved because %s\nURL: %s', error, url)
            return("Fail")
        except URLError as error:
            if isinstance(error.reason, socket.timeout):
                logging.error('socket timed out - URL %s', url)
                return("Fail")
            else:
                logging.error('some other error happened')
                return("Fail")
        else:
            logging.info('Access successful.')
            matches = re.findall(str(apacheCheck), response)
            if len(matches) == 0: 
                print ('apache2 text not found')
            else:
                print ('apache2 text found')
                return("Ok")
        return("Fail")

    else:
        print("Apache ERROR: Inject ID not found for " + cI + " of type: " + str(type(cI)))
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def grapherFunction():
    while (True): 
    #~~~~~~~~Variables~~~~~~~~#
        #Below Parameters on Injects.cnf. Must be same for ALL clients
        global ftpFile
        global ftpFileHash
        global ftpPath
        global serverFTPDir
        global ftpUSR
        global ftpPWD
        global apacheCheck
        global apacheWebsite
        global dataDirectory
        global mySQL_Query
        global smbUSR
        global smbPWD
        global smbSHR
        global smbSHRFile
        ######
        global injectSMBCurr
        global injectApacheCurr
        global injectSSHCurr
        global sshUSR
        global sshPWD
        global sshPRT
    #~~~~~~~~~~~~~~~~~~~~~~#
        config = CaseConfigParser(os.environ)
        config.read('Injects.cnf')

        injectSMBCurr = config.get('Injects', 'smbCurrInject')
        injectApacheCurr = config.get('Injects', 'apacheCurrInject')
        injectSSHCurr = config.get('Injects', 'sshCurrInject')

        checkInterval = int(config.get('General', 'checkInterval'))
        ftpFile = config.get('General', 'ftpFile')
        ftpFileHash = config.get('General', 'ftpFileHash')
        ftpPath = config.get('General', 'ftpPath') #Path on the client where the file to be checked is stored
        serverFTPDir = config.get('General', 'serverFTPDir')
        ftpUSR = config.get('General', 'ftpUSR')
        ftpPWD = config.get('General', 'ftpPWD')  
        apacheCheck = config.get('General', 'apacheCheck') #string to look for in apache2 page
        apacheWebsite = config.get('General', 'apacheWebsite') #page to look for for string
        dataDirectory = config.get('General', 'dataDirectory') #directory on server to store data
        mySQL_Query = config.get('General', 'mySQL_Query')
        smbUSR = config.get('General', 'smbUSR')
        smbPWD = config.get('General', 'smbPWD')
        smbSHR = config.get('General', 'smbSHR')
        sshUSR = config.get('General', 'sshUSR')
        sshPWD = config.get('General', 'sshPWD')
        sshPRT = int(config.get('General', 'smbPRT'))
    #~~~~~~~~~PLOT~~~~~~~~~# 
        fig = plt.figure(dpi=80)
        ax = fig.add_subplot(1,1,1)
        table_data=[[" "], ["Internet"], ["Apache2"], ["SMB"], ["SSH"]] # ["Internet"], ["Apache2"], ["SMB"], ["SSH"]
        for t in allTeams:
            table_data[0].append(t.getName())
            table_data[1].append(str(checkInternet (str(t.getAddress()))) + ":" + str(t.countUptime("internet", 1)))
            #table_data[1].append(str(checkFTP(str(t.getAddress()),"21", ftpFile, ftpFileHash)) + ":" + str(t.countUptime("ftp" , injectSMBCurr)))
            table_data[2].append(str(check_apache2(t.getAddress(), injectApacheCurr)) + ":" + str(t.countUptime("apache" , injectApacheCurr)))
            table_data[3].append(str(checkSMB(t.getAddress(), t.getName(), injectSMBCurr)) + ":" + str(t.countUptime("samba", injectSMBCurr)))
            table_data[4].append(str(checkSSH(t.getAddress(), sshPRT, sshUSR, sshPWD, injectSSHCurr)) + ":" + str(t.countUptime("ssh", injectSSHCurr)))
        table = ax.table(cellText=table_data, loc='center')
        table.set_fontsize(14)
        table.scale(1,4)
        ax.axis('off')
        plt.savefig("InjectSLA.png")
        time.sleep(checkInterval)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def main():
    grapherFunction()
   
if __name__ == "__main__":
    main()
