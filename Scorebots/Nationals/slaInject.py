import matplotlib.pyplot as plt 
import subprocess, platform, os
import hashlib
import urllib.request as urllib2
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
        self.apacheHIST = []
    def getName(self):
        return self.name
    def getAddress(self):
        return self.address
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
    Team('Computer2', '192.168.1.5')
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

def check_apache2(ip):
    apachestatus = "Fail"
    try:
        html_content = urllib2.urlopen("http://" + ip + "/" + apacheWebsite).read().decode('utf-8')
        matches = re.findall(str(apacheCheck), html_content);
        if len(matches) == 0: 
            print ('apache2 text not found')
            apachestatus = "Fail"
        else:
            print ('apache2 text found')
            apachestatus = "Ok"
    except Exception as e:
        print("apache2 exception: " + str(e))
    
    return (apachestatus)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def grapherFunction():
   while (True): 
        fig = plt.figure(dpi=80)
        ax = fig.add_subplot(1,1,1)
        table_data=[[" "], ["Internet"], ["FTP"], ["Apache2"] ]
        for t in allTeams:
            table_data[0].append(t.getName())
            table_data[1].append(str(checkInternet (str(t.getAddress()) )) + ":" + str(t.countUptime("internet")))
            table_data[2].append(str(checkFTP(str(t.getAddress()),"21", ftpFile, ftpFileHash)) + ":" + str(t.countUptime("ftp")))
            table_data[3].append(str(check_apache2(str(t.getAddress()))) + ":" + str(t.countUptime("apache")))
        table = ax.table(cellText=table_data, loc='center')
        table.set_fontsize(14)
        table.scale(1,4)
        ax.axis('off')
        plt.savefig("graphReliability.png")
        time.sleep(checkInterval)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def main():
    grapherFunction()
    #~~~~~~~~~~~~~~~~~~#
    import multiprocessing
    processes = [ 
    multiprocessing.Process(target=checkInternet()), 
    multiprocessing.Process(target=checkFileFTP()),
    multiprocessing.Process(target=check_apache2())

    ]
 
    if process.is_alive():
        p.terminate()

        for p in processes: 
            p.start()
        for q in processes: 
            q.join(5)


if __name__ == "__main__":
    main()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
