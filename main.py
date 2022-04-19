from ast import Bytes
from network.tcpserver import TcpServer

TcpServer(("0.0.0.0", 9339)).start_accept()