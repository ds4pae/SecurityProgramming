from PGP_All_Common import *

KEY_GEN_STATUS = False
alice_privatekey = './HybridAlice/aliceprivatekey.txt'
alice_publickey = './HybridAlice/alicepublickey.txt'
bob_publickey = './HybridAlice/received_bobpublickey.txt'
# 키 공유 프로세스 (tcp/ip 기반 공개키 공유 과정)

print("PGP : Alice")
choice = int(input("Input (0) RSA Key Generation, (1) Send public key, (2) Receive public key, (3) Exit : "))

while True:
    if choice == 0:
        KEY_GEN_STATUS = True
        PGP_Generate_Key_File(alice_privatekey, alice_publickey)
    if choice == 1:
        PGP_Client_Send_File_byUDP('localhost', 6001, alice_publickey)
    if choice == 2:
        PGP_Server_Receive_File_byUDP('localhost', 7001, bob_publickey)
    if choice == 3:
        break
    if KEY_GEN_STATUS == False:
        choice = int(input("Input (0) RSA Key Generation, (1) Send public key, (2) Receive public key, (3) Exit : "))
    else:
        choice = int(input("Input (1) Send public key, (2) Receive public key, (3) Exit : "))
