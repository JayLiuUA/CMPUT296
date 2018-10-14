# Name: Xiaohui Liu
# The date: Feb 19, 2018
# The names of any students you consulted with: Yuan Wang

# ---------------------------------------------------------------------------
#    URL parser  Copyright (C) 2018  Xiaohui Liu
#    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#    This is free software, and you are welcome to redistribute it
#    under certain conditions; type `show c' for details.
# ---------------------------------------------------------------------------

#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    
    def get_host_port(self,url):
        host = urllib.parse.urlparse(url).hostname
        port = urllib.parse.urlparse(url).port
        path = urllib.parse.urlparse(url).path
        return host, port, path

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            # receive data (string) from socket, 1024 is max data size
            part = sock.recv(1024)          
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        code = 500
        body = "" 
        host, port, path = self.get_host_port(url)
        if port == None:
            # default value of port is 80    
            port = 80    
        if len(path) == 0:
            path = '/'
            data = "GET "+ path + " HTTP/1.1\r\nHost: "+str(host)+ "\r\n" + "Connection: close" + "\r\n\r\n"
        else:
            data = "GET "+str(path) + " HTTP/1.1\r\nHost: "+str(host)+ "\r\n" + "Connection: close" + "\r\n\r\n"
        self.connect(host,port)
        self.sendall(data)
        response = self.recvall(self.socket)
        responseList = response.splitlines()
        firstLine = responseList[0]
        split = firstLine.split(' ', 2)
        # version = split[0], message = split[2]
        code_str = split[1]  
        code = int(code_str)
        
        for i in range(len(responseList)):
            # try to find the new line seperating headers and body
            if responseList[i] == '':
                # if new line is found, put things after it into body
                body = body.join(responseList[i+1:])
                
        self.close()
        return HTTPResponse(code, body)
    
    def POST(self, url, args=None):
        code = 500
        body = ""
        host, port, path = self.get_host_port(url)
        post = "POST "+str(path)+" HTTP/1.1\r\nHost: "+str(host)+"\r\nContent-Type: application/x-www-form-urlencoded"        
        
        if args == None:        # if there is no arguments
            request = "POST "+str(path)+" HTTP/1.1\r\nHost: "+str(host)+"\r\n"+"content-Length:0" + "\r\n\r\n" 
        else:
            data = urllib.parse.urlencode(args)
            contentLength = "\r\ncontent-Length: " + str(len(data))
            request = post + contentLength + "\r\n\r\n" + data            

        if port == None:
            port=80
            
        self.connect(host,port)
        self.sendall(request)    
        
        response = body + self.recvall(self.socket)
        # split response into 2 parts by finding the empty line
        split = response.split('\r\n\r\n')
        version, code_str, message=re.split(r'\s+',split[0],2)
        code = int(code_str)        # convert code to int
        body = split[1]

        self.close()        
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
        
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))