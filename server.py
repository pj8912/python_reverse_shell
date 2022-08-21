import socket
import sys

def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9999
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print("error "+ msg)


def bind_socket():
    try:
        global host
        global port
        global s 

        print("Bindining the Port" +str(port))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host,port))
        s.listen(5)

    except socket.error as msg:
        print(str(msg))
 

def accept_connection():
    conn, address = s.accept()
    print("connected to "+str(address[0])+ " at "+ str(address[1]))
    send_command(conn)
    conn.close()


#send to client
#message will be in form of bytes

def send_command(conn):
    while True:
        cmd = input()
        if cmd == 'quit':
            conn.close()
            s.close()
            sys.exit()

        if len(str(cmd.encode('utf-8'))) > 0:
            conn.send(cmd.encode('utf-8'))
            client_response = conn.recv(1024)
            print(client_response.decode('utf-8'), end="")


def main():

    try:
        create_socket()
        bind_socket()
        accept_connection()
    except KeyboardInterrupt:
        sys.exit(0)

main()

    
