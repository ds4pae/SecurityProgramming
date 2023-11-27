# -*- coding: utf8 -*-
import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import pickle

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 8888
BUFSIZE = 2048

client_sock.connect((host, port))
#Tell server that connection is OK
client_sock.sendall(b"Client: OK")

#Receive public key string from server
server_string = client_sock.recv(BUFSIZE)

#Remove extra characters
server_string = server_string.decode('utf-8')
server_string = server_string.replace("public_key=", '')
server_string = server_string.replace("\r\n", '')

#Convert string to key
print(server_string)
server_public_key = RSA.importKey(server_string)

#Encrypt message and send to server
message = b"This is my secret message."
RSAObj = PKCS1_OAEP.new(server_public_key)
encrypted = RSAObj.encrypt(message)
encrypted = pickle.dumps(encrypted)
print("Encrypted Message: ", encrypted)
client_sock.send(encrypted)

#Server's response
server_response = client_sock.recv(BUFSIZE)
server_response = server_response.decode('utf-8')
print(server_response)
server_response = server_response.replace("\r\n", '')
if server_response == "Server: OK":
    print("Server decrypted message successfully")

#Tell server to finish connection
client_sock.sendall(b"Quit")
client_sock.close()