#!/usr/bin/env python3
import os
import sys
import time
import subprocess
import tkinter as tk
from tkinter import *

# --- functions ---# 

def submit():
    data = e.get()

    if data in already_submitted:
        print('Sorry already submitted:', data)  

    else:  
        print('Submit:', data)
        testString = ''.join(data)
        print("Test string: " + testString)

        try:
            ourUser.append((testString.split(":")[0]))
            ourMode.append((testString.split(":")[1]))
            ServIP.append((testString.split(":")[2]))   

            #if ((str(ourMode[1])) != server and (str(ourMode[1] != single))):
            #    raise CustomException("must be server or single")

            already_submitted.append(data)
            x.config(text=already_submitted)
            e.config({"background": "green"})
            b['state'] = 'disable'
            os.system("mkdir /etc/scorebot 2>/dev/null")
            os.system("touch /etc/scorebot/.usr.dat 2>/dev/null")
            os.system("echo " + data + " > /etc/scorebot/.usr.dat")
            time.sleep(2)
            root.destroy()
        except:  
            x.config(text="Malformed Input. You entered: " + testString)
            e.config({"background": "red"}) 

        del already_submitted [:]

def check(event):
    #data = event.widget.get()
    data = e.get()

    if data in already_submitted:
        b['state'] = 'disable'
    else:
        b['state'] = 'normal'
##############
# don't submit empty string        
already_submitted = ['']
ourUser = ['']
ourMode = ['']
ServIP = ['']

root = tk.Tk()
root.title('Scoring Program')

w = tk.Label(root, text="Syntax = username:[server/single]:server_IP:server_port\n")
w.pack(side = TOP)

g = tk.Label(root, text="If [single] is selected, leave the other columns as none.")
g.pack(side = TOP)

q = tk.Label(root, text="Score via server: joe:server:192.168.5.5:443")
q.pack(side = TOP)

v = tk.Label(root, text="Example: none:single:none:none")
v.pack(side = TOP)

x = tk.Label(root, text=already_submitted)
x.pack(side = BOTTOM)

e = tk.Entry(root)
e.pack()
e.bind('<KeyRelease>', check)
b = tk.Button(root, text="Submit", command=submit, state='disable')
b.pack()
root.mainloop()
###########################
