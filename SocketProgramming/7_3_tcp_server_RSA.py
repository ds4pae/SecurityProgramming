# -*- coding: utf8 -*-

import socket
from Crypto.PublicKey import RSA
from Crypto import Random
import pickle

#Generate private and public keys
random_generator = Random.new().read
private_key = RSA.generate(1024, random_generator)
f = open('privateKey.txt','wb')
f.write(bytes(private_key.exportKey()))
f.close()
public_key = private_key.publickey()

print(private_key)
HOST = 'localhost'
PORT = 8888
BUFSIZ = 2048
ADDR = (HOST, PORT)

if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(ADDR)
    server_socket.listen(5)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_sock, addr = server_socket.accept()

    data = client_sock.recv(BUFSIZ)
    data = data.decode('utf-8')
    print(data)
    data = data.replace("\r\n", '')  # remove new line character

    if data == "Client: OK":
        client_sock.send(b"public_key=" + public_key.exportKey() + b"\n")
        print("Public key sent to client.")

    while True:
        data = client_sock.recv(BUFSIZ)
        print("Received:\nEncrypted message = " + str(data))
        if data == b"Quit":
            print("Decrypted message = ", data.decode('utf-8'))
            break

        encrypted = pickle.loads(data)
        decrypted = private_key.decrypt(encrypted)

        client_sock.send(b"Server: OK")
        print("Decrypted message = ", decrypted.decode('utf-8'))

    client_sock.close()
    server_socket.close()