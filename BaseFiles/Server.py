#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import os,sys
import time
import subprocess
import requests
import ssl
import numpy as np
###########
class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers() 
    
    def ParseData(self,d):
        OutputRaw="/home/cyber/Desktop/OutputRaw.csv"
        FinalOutput="/home/cyber/Desktop/Output.csv"
        dUSR = str(d.split(":")[0])
        dSCORE = str(d.split(":")[1])
        dTIME = int(d.split(":")[2]) 
        dKEY = str(d.split(":")[3]) #key so anyone can't just run curl command(not very secure, but doubt they'll exploit it. KEY is in the obfuscated script on client)
        if (dKEY == "cool"):
            print("keys match")
            with open(OutputRaw, 'a') as file:
                if (abs((dTIME) - int((time.time() / 60))) <= 3 ): #if user sent time = our time(so they can't just change their PC time)
                    print("Times match")
                    file.write(dUSR + "," + dSCORE +"," + str(dTIME) + "\n")  #Force time on client PC  
                    os.system('''awk 'BEGIN{ OFS = FS = "," } NR == 1 { base = $3 } { $3 -= base; print }'  < ''' + OutputRaw + ''' > ''' + FinalOutput)
                else:
                    print("Times do not match. Client Time: " + str(dTIME) + " SERVER TIME: " + str(int((time.time() / 60))))
               

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        #POST SYNTAX ON CLIENT:  curl -X POST -d 'cyber:43232' http://localhost:443
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))
        self._set_response()
        PRQST = (post_data.decode('utf-8'))
        print(PRQST)
        self.ParseData(PRQST)
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))


def run(server_class=HTTPServer, handler_class=S, port=80):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
