from socket import socket, AF_INET, SOCK_DGRAM
maxsize = 4096
hostname = 'localhost'
PORT = 12350
ADDRESS = (hostname, PORT)

server_sock = socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
server_sock.bind(ADDRESS)

while True:
    data, addr = server_sock.recvfrom(maxsize)
    print("Data from Client : ", data.decode())
    resp = "UDP server sending data"
    server_sock.sendto(resp.encode('utf-8'),addr)