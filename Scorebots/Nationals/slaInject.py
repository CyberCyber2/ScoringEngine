#!/usr/bin/env python3
#runs on the SERVER
import matplotlib.pyplot as plt 
import subprocess, platform, os
import hashlib
import urllib.request as urllib2
import re
import time
from difflib import SequenceMatcher
#
###############CONFIG###################
ftpFile = "FTPCHECK.txt"
ftpFileHash = "da39a3ee5e6b4b0d3255bfef95601890afd80709"
ftpPath = "/home/joe/" #Path on the client where the file to be checked is stored
apacheCheck = "Check2132" #string to look for in apache2 page
apacheWebsite = "index.html" #page to look for for string
checkInterval = 5
dataDirectory = "/home/server/Desktop/data/" #directory on server to store data
########################################
class Team:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.internetHIST = []
        self.ftpHIST = []
        self.apacheHIST = []
    def getName(self):
        return self.name
    def getAddress(self):
        return self.address    
    def countUptime(self, service): 
        self.internetFileData = "/home/server/Desktop/data" + self.name + "INTERNETHIST.dat" #storage location for previous history. Ex: Computer1INTERNETHIST.dat
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
            writeToFile(self.internetFileData, self.internetHIST)
            return internetReliability
 
            #~~~~~~~~~~~~~~~~#
 
        if service == "ftp":
            if (checkFTP(str(self.getAddress()),"21",ftpFile, ftpFileHash) == "Ok"):
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
            if (check_apache2(str(self.getAddress())) == "Ok"):
                self.apacheHIST.append("1")
                print("apache2 reliable, added 1")
                print(self.apacheHIST)
            else:
                self.apacheHIST.append("0")
                print("apache2 unreliable, added 0")
                print(self.apacheHIST)
            apacheReliability = str(self.apacheHIST.count("1") + self.apacheHIST.count("0") * (-5))
            return apacheReliability
########################################################################
allTeams = [
    Team('Erdie', '127.0.0.1'),
    Team('Matt', '127.0.0.1')
]
########################################################################
def similar(a, b): #Just incase the hash has an extra space, don't feel like removing space
    return SequenceMatcher(None, a, b).ratio()
 
def readData(filename):
    with open(filename) as f:
        lines = [line.rstrip() for line in f]
 
def writeToFile(filename, dataList):
    with open('filename', 'w') as f:
        for item in dataList:
            f.write("%s\n" % item)
#~~~~~~~~~~~~~~PING~~~~~~~~~~~~~~~#
def checkInternet(ip):
    hostname = ip
    response = os.system("ping -c 1 " + hostname)
    if response == 0:
        pingstatus = "Ok"
    else:
        pingstatus = "Fail"
    return pingstatus
#~~~~~~~~~~~~~~FTP~~~~~~~~~~~~~~~#
import ftplib
#You must place a checkfile in the ftp directory on the CLIENT
#checkfile: file to look for on CLIENT
#filehash: correct hash to check for
def checkFTP(ip, port, checkfile, filehash):
    try:
        ftp = ftplib.FTP(ip) 
        ftp.login("joe", "joe")
        ftp.cwd(ftpPath)
        ftp.retrbinary("RETR " + checkfile, open(checkfile, 'wb').write)
        f = "/home/cyber/Desktop/" + checkfile #FILE DOWNLOADED FROM CLIENT TO SERVER
        checkHash = os.popen(("sha1sum " + f + "| cut -d' ' -f1")).read()
        if (float(similar(checkHash,filehash)) >= 0.9):
            print("FTP hashes match")
            return ("Ok")
        else:
            print("Client Hash: " + checkHash + " Server Hash: " + ftpFileHash)
            return ("Fail")
        ftp.quit()
    except Exception as e:
        print("FTP hash exception: " + str(e) + " for " + str(ip))
        return ("Fail")
#~~~~~~~~~~~~~~SMTP~~~~~~~~~~~~~~~#
from smtplib import SMTP
def check_smtp(ip, port):
    try:
        smtp = SMTP(ip, port)
        smtp.quit()
        return ("Ok")
    except Exception as e:
        return ("Fail")
#~~~~~~~~~~~~~~APACHE2~~~~~~~~~~~~~~~#
#check to see if a certain text appears on the webserver
def check_apache2(ip):
    try:
        html_content = urllib2.urlopen("http://" + ip + "/" + apacheWebsite).read().decode('utf-8')
        matches = re.findall(str(apacheCheck), html_content);
        if len(matches) == 0: 
            print ('apache2 text not found')
            return ("Fail")
        else:
            print ('apache2 text found')
            return ("Ok")
    except Exception as e:
        print("apache2 exception: " + str(e))
        return ("Fail")
#~~~~~~~~~~~~~~DNS~~~~~~~~~~~~~~~#
def check_dns(ip, port, query, query_type, answer):
    res = resolver.Resolver()
    res.nameservers = [ip]
    try:
        query_answer = str(res.query(query, query_type).rrset[0])
        print("[DEBUG-DNS] DNS answered", query_answer)
        if answer != query_answer:
            return (0, "DNS server returned incorrect answer " +\
                        query_answer + " to query " + query +". Correct \
                        answer was " + answer + ".")
        return ("Ok")
    except Exception as e:
        return ("Fail")
#~~~~~~~~~~~~~~RDP~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~SMB~~~~~~~~~~~~~~~#
def check_smb(ip, port, anon, share, checkfile, filehash, domain):
    path = '//{}/{}'.format(ip, share)
    if checkfile and filehash:
        tmpfile = path + "tmpfiles/smb-%s-%s-%s-checkfile" % (share, ip, checkfile)
        cmd = 'get "{}" "{}"'.format(checkfile, tmpfile)
        smbcli = ['smbclient', "-N", path, '-c', cmd]
        if domain:
            smbcli.extend(['-W', domain])
        #try:
        print("[DEBUG-SMB] Grabbing file for", ip)
        output = subprocess.check_output(smbcli, stderr=subprocess.STDOUT)
        with open(tmpfile, "rb") as f:
            content = f.read()
            checkhash = hashlib.sha1(content).hexdigest();
        if checkhash != filehash:
            return(0, "Hash %s does not match %s." % (checkhash, filehash))
        return 1, None
        #except Exception as e:
        #    return 0, str(e)
    else:
        print("[DEBUG-SMB] Trying anonymous/noauth for", ip)
        smbcli = ['smbclient', "-N", "-L",  path]
        if domain:
            smbcli.extend(['-W', domain])
        try:
            output = subprocess.check_output(smbcli, stderr=subprocess.STDOUT)
            return ("Ok")
        except Exception as e:
            return ("Fail")
#~~~~~~~~~~~~~~SSH~~~~~~~~~~~~~~~#
#from paramiko import client, RSAKey
#from paramiko.ssh_exception import *
#import socket
def check_ssh(ip, port, user, private_key):
    try:
        cli = client.SSHClient()
        cli.load_host_keys("/dev/null")
        cli.set_missing_host_key_policy(client.AutoAddPolicy())
        if private_key and user:
            print("[DEBUG-SSH] Trying pubkey auth for", ip)
            k = RSAKey.from_private_key_file(path + "checkfiles/" + private_key)
            cli.connect(ip, port, user, banner_timeout=20, timeout=20, auth_timeout=20, pkey=k)
        else:
            cli.connect(ip, port, "root", "Password3#", banner_timeout=20, timeout=20, auth_timeout=20)
        cli.close()
        return ("Ok")
    except Exception as e:
        if str(e) == "Authentication failed." and not private_key:
            return ("Ok")
        return ("Fail")
########################################################################
def main():
    while (True): 
        fig = plt.figure(dpi=80)
        ax = fig.add_subplot(1,1,1)
        table_data=[[" "], ["Internet"], ["FTP"] ]
        for t in allTeams:
            table_data[0].append(t.getName())
            table_data[1].append(str(checkInternet (str(t.getAddress()) )) + ":" + str(t.countUptime("internet")))
            table_data[2].append(str(checkFTP(str(t.getAddress()),"21", ftpFile, ftpFileHash)) + ":" + str(t.countUptime("ftp")))
            #table_data[1].append(str(check_apache2(str(t.getAddress()))) + ":" + str(t.countUptime("apache")))
        table = ax.table(cellText=table_data, loc='center')
        table.set_fontsize(14)
        table.scale(1,4)
        ax.axis('off')
        plt.savefig("InjectSLA.png")
        time.sleep(checkInterval)
 
if __name__ == "__main__":
    main()
 
################################
import multiprocessing


def checkInternet(): pass

process = multiprocessing.Process(target=checkInternet())
process.start() # start the function
process.join(10) # wait max 10 seconds for functionA to finish

if process.is_alive():
  # The function is still running
  p.terminate()

for p in processes:
  p.start()
for p in processes:
  p.join(10)
