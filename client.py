    
import socket
from threading import Thread

IP = "127.0.0.1"
PORT = 1010
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP,PORT))

def send_msg():
    message = input("Message: ")
    client.send(message.encode("utf-8"))
    if message == "exit":
        client.close()
        exit()
    send_msg()


def recieve_msg():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            print(message)
        except OSError:
            break    
          
Thread(target = recieve_msg).start()
Thread(target = send_msg).start()
