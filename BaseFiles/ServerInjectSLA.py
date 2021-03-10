import matplotlib.pyplot as plt 
import subprocess, platform, os
import hashlib
import urllib.request
import re
import time
from difflib import SequenceMatcher
###############CONFIG###################
checkInterval = 5
ftpFile = "FTPCHECK.txt"
ftpFileHash = "da39a3ee5e6b4b0d3255bfef95601890afd80709"
ftpPath = "/home/joe/" #Path on the client where the file to be checked is stored
apacheCheck = "Check2132" #string to look for in apache2 page
apacheWebsite = "index.html" #page to look for for string
checkInterval = 5
dataDirectory = "/home/server/Desktop/data/" #directory on server to store data
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
class Team:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.ftpHIST = []
        self.internetHIST = []
        self.apacheHIST = []
    def getName(self):
        return self.name
    def getAddress(self):
        return self.address
    def getApache(self):
        return str("test")
    def countUptime(self, service): 

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
            print("Service is apache")
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

allTeams = [
    Team('Computer1', '127.0.0.1'),
    Team('Computer2', '10.4.2.19')
]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def similar(a, b): #Just incase the hash has an extra space, don't feel like removing space
    return SequenceMatcher(None, a, b).ratio()
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

def checkFTP(ip, port, checkfile, filehash):
    ftpstatus = "Fail"
    try:
        ftp = ftplib.FTP(ip) 
        ftp.login("joe", "joe")
        ftp.cwd(ftpPath)
        ftp.retrbinary("RETR " + checkfile, open(checkfile, 'wb').write)
        f = "/home/cyber/Desktop/" + checkfile #FILE DOWNLOADED FROM CLIENT TO SERVER
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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
from urllib.error import HTTPError, URLError
import logging
import socket
def check_apache2(ip):
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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def grapherFunction():
   while (True): 
        fig = plt.figure(dpi=80)
        ax = fig.add_subplot(1,1,1)
        table_data=[[" "], ["Apache2"] ]
        for t in allTeams:
            table_data[0].append(t.getName())
           # table_data[1].append(str(checkInternet (str(t.getAddress()) )) + ":" + str(t.countUptime("internet")))
            #table_data[2].append(str(checkFTP(str(t.getAddress()),"21", ftpFile, ftpFileHash)) + ":" + str(t.countUptime("ftp")))
            table_data[1].append(str(t.getApache()) + ":" + str(t.countUptime("apache")))
        table = ax.table(cellText=table_data, loc='center')
        table.set_fontsize(14)
        table.scale(1,4)
        ax.axis('off')
        plt.savefig("InjectSLA.png")
        time.sleep(checkInterval)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def main():
    grapherFunction()
   
if __name__ == "__main__":
    main()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
