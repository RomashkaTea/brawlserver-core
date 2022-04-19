import socket, select
from network.connection import Connection

class TcpServer:
    def __init__(self, addr):
        self.addr = addr
        self.socket = socket.socket()
        self.socket.setblocking(0)
        self.inputs = {self.socket: None}
    
    def disconnect(self, socket):
        if socket in self.inputs:
            print("disconnect!")
            socket.close()
            self.inputs.pop(socket)

    def start_accept(self):
        self.socket.bind(self.addr)
        self.socket.listen()
        print("TCP server started!")
        while True:
            read_fds, write_fds, except_fds = select.select(self.inputs, [], self.inputs) # [] - output
            for i in read_fds:
                if i == self.socket:
                    client, addr = self.socket.accept()
                    client.setblocking(0)
                    print(f"new connection from {addr[0]}:{addr[1]}")
                    self.inputs[client] = Connection(client)
                else:
                    if i in self.inputs:
                        try:
                            result = self.inputs[client].receive_message()
                            if result == -1:
                                self.disconnect(i)
                        except: self.disconnect(i)