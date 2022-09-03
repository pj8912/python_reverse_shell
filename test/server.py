import socket, sys

class Server:

    def __init__(self, host, port):
        

        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            print("Bindining the Port " +str(self.port))
            self.sock.bind((host, port))
            self.sock.listen(5)
            self.accept_connection()
        except socket.error as msg:
            print(str(msg))





    def accept_connection(self):
        
        conn, address = self.sock.accept()
        
        print("connected to "+ str(address[0])+ " at " + str(address[1]))
        
        self.send_command(conn)
        
        conn.close()



    def send_command(self, conn):
        while True:
            cmd = input()
            if cmd == 'quit':
                conn.close()
                self.sock.close()
                sys.exit()
            command = cmd.encode('utf-8')
            if len(str(command)) > 0:
                conn.send(command)
                client_response = conn.recv(1024)
                print(client_response.decode('utf-8'), end="")


try:
    server = Server("", 9999)
except KeyboardInterrupt:
    sys.exit(0)

