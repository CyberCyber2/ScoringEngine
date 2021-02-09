Icons:
This directory contains Icons that a future version of install.py should set as the icons for the files being installed.

install.py:
This file MUST be installed on the Linux image wanted to be scored. It downloads dependencies, downloads the scorebot from github(change the link in the file to the current version of the scorebot), and obfuscates it using "emojify"

scorebot.py:
The template scorebot, no vulnerabilities are scored here. It does not need to be installed on the Linux image since install.py will do that for you.

Server.py:
ONLY put this on the server if you want one. A server is a separate Linux machine which the clients send their scores to(if configured). The scorebot.py will read the settings in TeamInfo.py to tell whether to send scores or not. If you are not using a Server, don't bother with configuring a server(TeamInfo.py is still needed).

TeamInfo.py:
A GUi where you enter server settings. This is downloaded by install.py on the host to be scored. The syntax is-->

TeamName:Mode:ServerIP:ServerPort

If you are not using a server, just type in none:none:none:none. 
