from PGP_All_Common import *

alice_privatekey = './HybridAlice/aliceprivatekey.txt'
alice_publickey = './HybridAlice/alicepublickey.txt'
bob_publickey = './HybridAlice/received_bobpublickey.txt'
# 키 공유 프로세스 (tcp/ip 기반 공개키 공유 과정)
"""
PGP_Generate_Key_File(alice_privatekey, alice_publickey)
PGP_Server_Send_File('localhost', 6001, alice_publickey)
PGP_Client_Receive_File('localhost', 7001, bob_publickey)
"""
alice_plaintext = './HybridAlice/plaintext.txt'
sig_MSG_alice = './HybridAlice/sig_MSG_Alice.txt'
Generate_DigSig_On_Hashed_File(alice_plaintext, alice_privatekey, sig_MSG_alice)

alice_output = './HybridAlice/outputAlice.txt'
Generate_AES_Enc_On_DigSig_Plus_Key(sig_MSG_alice, bob_publickey, alice_output)

alice_output_b64 = './HybridAlice/outputAlice_b64.txt'
B64Encoding(alice_output, alice_output_b64)
#PGP_Server_Send_File('localhost', 8001, alice_output_b64)
PGP_Client_Send_File_byUDP('localhost', 9001, alice_output_b64)