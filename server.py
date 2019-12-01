import socket
import sys
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
host = ""
port = 15600
connexion_principale = None

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



def socket_create():
    try:
        global host
        global port
        global connexion_principale
        connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print("Socket creation error ", msg)

def socket_bind():
    try:
        global host
        global port
        global connexion_principale
        print("binding socket to port ", port)
        connexion_principale.bind((host,port))
        connexion_principale.listen(5)
    except socket.error as msg:
        print("Socket binf error ", msg)
        socket_bind()

def socket_accept():
    global host
    global port
    global connexion_principale
    connexion_avec_client , infos = connexion_principale.accept()
    print("client information , IP : ", infos[0], ' | Port : ', infos[1])
    send_command(connexion_avec_client)
    connexion_avec_client.close()

def send_command(connexion_avec_client):
    global cipher
    global cipher_clear

    while True:
        cmd = input()

        if cmd == "quit":
            connexion_avec_client.close()
            connexion_principale.close()
            sys.exit()
        if len(cmd.encode())  > 0:
            cmd = cipher.encrypt(cmd.encode())
            connexion_avec_client.send(cmd)
            client_respon = connexion_avec_client.recv(16384)
            data_encrypted = client_respon
            client_respon = cipher_clear.decrypt(client_respon).decode()
            print("---- donnée cryptée -----")
            print(data_encrypted)
            print("---- donnée cryptée -----")
            print(client_respon, end="")

def main():
    global cipher
    global cipher_clear

    cipher,cipher_clear = key_initialization()
    socket_create()
    socket_bind()
    socket_accept()
    #send_command()
main()