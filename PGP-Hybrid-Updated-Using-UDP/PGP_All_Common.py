from Crypto.PublicKey import RSA
import socket                   # Import socket module
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP


def PGP_Generate_Key_File(priKey_filename, pubKey_filename, keySize=2048):
    privatekey = RSA.generate(keySize)
    f = open(priKey_filename,'wb')
    f.write(bytes(privatekey.exportKey()))
    f.close()
    publickey = privatekey.publickey()
    f = open(pubKey_filename,'wb')
    #f.write(bytes(publickey.exportKey('PEM'))); f.close()
    f.write(bytes(publickey.exportKey()))
    f.close()
    return


def PGP_Server_Send_File(host_name, port_Num, send_filename):
    port = port_Num  # Reserve a port for your service.
    host = host_name  # ex : 'localhost' Get local machine name
    server_socket = socket.socket()  # Create a socket object
    server_socket.bind((host, port))  # Bind to the port
    server_socket.listen(15)  # Now wait for client connection.
    print('Server listening....')

    while True:
        client_socket, addr = server_socket.accept()  # Establish connection with client.
        print('Got connection from', addr)
        data = client_socket.recv(1024)
        print('Server received', repr(data))

        filename = send_filename  # './HybridAlice/received_alicepublickey.txt'
        f = open(filename, 'rb')
        l = f.read(1024)
        while (l):
            client_socket.send(l)
            print('Sent ', repr(l))
            l = f.read(1024)
        f.close()
        print('Done sending')
        client_socket.send(b'')
        break
    print("Sent %s file from Server to Client!!" % send_filename)
    client_socket.close()
    server_socket.close()


def PGP_Client_Receive_File(host_name, port_Num, receive_filename):
    port = port_Num  # Reserve a port for your service.
    host = host_name  # ex : 'localhost' Get local machine name
    client_socket = socket.socket()  # Create a socket object
    client_socket.connect((host, port))
    client_socket.send(b"Client OK")

    f = open(receive_filename, 'wb') # './HybridAlice/received_bobpublickey.txt'
    print('file opened')

    while True:
        print('Receiving data...')
        data = client_socket.recv(1024)
        print('Received ', repr(data))
        if not data:
            break
        f.write(data)

    print("Receive %s file from Server to Client!!" % receive_filename)
    f.close()
    client_socket.close()


def PGP_Server_Receive_File_byUDP(host_name, port_Num, receive_filename):
    global msg
    port = port_Num  # Reserve a port for your service.
    host = host_name  # ex : 'localhost' Get local machine name
    server_addr_port = (host, port)
    buffer_size = 1024

    udp_server_socket = socket.socket(family=socket.AF_INET, type= socket.SOCK_DGRAM)  # Create a socket object
    udp_server_socket.bind(server_addr_port)  # Bind to the port
    #udp_server_socket.setblocking(False)  # Now wait for client connection.
    print('UDP Server listening....')

    byte_addr_pair = udp_server_socket.recvfrom(buffer_size)
    print("Receive File: {}".format(byte_addr_pair[0]))
    print("Sender IP: {}".format(byte_addr_pair[1]))

    f = open(receive_filename, "wb")
    byte_addr_pair = udp_server_socket.recvfrom(buffer_size)
    try:
        while(byte_addr_pair[0]):
            client_msg = "msg from client : {} bytes".format(len(byte_addr_pair[0]))
            client_ip = "Sender IP : {} ".format(byte_addr_pair[1])
            print(client_msg)
            print(client_ip)
            f.write(byte_addr_pair[0])  ## 수신한 데이터를 파일에 쓰기..
            udp_server_socket.settimeout(2)
            byte_addr_pair = udp_server_socket.recvfrom(buffer_size)
    except socket.timeout:
        f.close()
        udp_server_socket.close()


def PGP_Client_Send_File_byUDP(host_name, port_Num, send_filename):
    server_port = port_Num  # Reserve a port for your service.
    server_host = host_name  # ex : 'localhost' Get local machine name
    server_addr_port = (server_host, server_port)
    buffer_size = 1024
    udp_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)  # Create a socket object

    udp_client_socket.sendto(send_filename.encode(), server_addr_port) # 보내고자 하는 파일 이름 전송

    f = open(send_filename, 'rb')
    print('{} file opened'.format(send_filename))
    msg_from_client = f.read(buffer_size)
    bytes_to_send = bytes(msg_from_client)

    while (bytes_to_send):
        if (udp_client_socket.sendto(bytes_to_send, server_addr_port)):
            print("Sending Data...")
            msg_from_client = f.read(buffer_size)
            bytes_to_send = bytes(msg_from_client)

    f.close()
    print('{} file sent using UDP OK...'.format(send_filename))
    udp_client_socket.close()
    print('UDP Client Socket Closed....')


def Generate_DigSig_On_Hashed_File(input_filename, sender_prikey_filename, output_filename):
    f = open(input_filename, 'rb')  #'./HybridAlice/plaintext.txt'
    plaintext = f.read()
    f.close()
    privatekey = RSA.importKey(open(sender_prikey_filename, 'rb').read())  #'./HybridAlice/aliceprivatekey.txt'
    myhash = SHA256.new(plaintext)  # Generate Hash
    signature = pkcs1_15.new(privatekey)  # Signature algo
    sigVal = signature.sign(myhash)  # signature value
    print("Length of Signature: ", len(sigVal))
    print("Signature: ", sigVal)
    output = sigVal + plaintext  ## concatnate message
    f = open(output_filename, 'wb') #'./HybridAlice/sig_MSG_Alice.txt'
    f.write(bytes(output))
    f.close()


def Verify_DigSig_On_Hashed_File(input_filename, receiver_pubkey_filename):
    f = open(input_filename, 'rb')
    sig_MSG = f.read()
    f.close()

    publickey = RSA.importKey(open(receiver_pubkey_filename, 'rb').read())
    cipherrsa = pkcs1_15.new(publickey)

    print("Signature: ", sig_MSG[:256])
    print("PlainText: ", sig_MSG[256:])

    myhash = SHA256.new(sig_MSG[256:])

    try:
        cipherrsa.verify(myhash, sig_MSG[:256])
        # 검증 결과 이상이 없으면 None 값이 리턴되고, 오류가 있는 경우 except 문 실행함...
        print("Signature Verification Result : True")
        f = open("HybridBob/received_plaintext.txt", "wb")
        f.write(sig_MSG[256:])
        f.close()
        print("Received Plaintext File Created!!!")

    except (ValueError, TypeError):
        print("Signature Verification Result : False")

def Generate_AES_Enc_On_DigSig_Plus_Key(sig_MSG_filename, receiver_pubkey_filename, output_filename):
    sessionkey = Random.new().read(32)  # 256 bit
    print("Session Key: ", sessionkey)
    # encryption AES of the message
    f = open(sig_MSG_filename, 'rb')  ### signature.txt || plaintext
    plaintext = f.read()
    f.close()
    iv = Random.new().read(16)  # 128 bit
    print("IV: ", iv)
    obj = AES.new(sessionkey, AES.MODE_CFB, iv)
    ciphertext = iv + obj.encrypt(plaintext)
    print("Cipher: ", ciphertext)

    # encryption RSA of the session key
    publickey = RSA.importKey(open(receiver_pubkey_filename, 'rb').read())
    cipherrsa = PKCS1_OAEP.new(publickey)
    enc_sessionkey = cipherrsa.encrypt(sessionkey)
    print("Length of encrypted session key: ", len(enc_sessionkey))  #### Length of session key: 256 byte
    print("Encrypted Session Key:", enc_sessionkey)
    f = open(output_filename, 'wb')
    f.write(bytes(enc_sessionkey))
    f.write(bytes(ciphertext))
    f.close()



def Generate_AES_Dec_For_DigSig_Plus_Key(sig_MSG_filename, sender_prikey_filename, output_filename):
    ENC_SESSION_KEY_SIZE = 256  # 256 * 8 = 2048 bit

    f = open(sig_MSG_filename, 'rb')  ### signature.txt || plaintext
    outputAlice = f.read()
    f.close()

    # decryption session key
    privatekey = RSA.importKey(open(sender_prikey_filename, 'rb').read())
    cipherrsa = PKCS1_OAEP.new(privatekey)

    sessionkey = cipherrsa.decrypt(outputAlice[:ENC_SESSION_KEY_SIZE])
    print("Decrypted Session Key: ", sessionkey)
    ciphertext = outputAlice[ENC_SESSION_KEY_SIZE:]

    iv = ciphertext[:16]
    print("Extracted IV: ", iv)
    obj = AES.new(sessionkey, AES.MODE_CFB, iv)
    plaintext = obj.decrypt(ciphertext[16:])
    f = open(output_filename, 'wb')
    f.write(bytes(plaintext))
    f.close()


def B64Encoding(fromFile, toFile):
    ff = open(fromFile, 'rb')
    l = ff.read(768)   # 3byte * 256 = 768
    tf = open(toFile, 'wb')
    while(l):
        l = base64.b64encode(l)
        tf.write(l)
        l = ff.read(768)
    tf.close()
    ff.close()


def B64Decoding(fromFile, toFile):
    ff = open(fromFile, 'rb')
    l = ff.read(1024)   # 4byte * 256 = 1024
    tf = open(toFile, 'wb')
    while(l):
        l = base64.b64decode(l)
        tf.write(l)
        l = ff.read(1024)
    tf.close()
    ff.close()
