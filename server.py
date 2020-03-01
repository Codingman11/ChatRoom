import socket
from threading import Thread


IP = "127.0.0.1"
PORT = 1010

clientAddress = {}
clientName = {}


def messages(client_server, address):
    name = client_server.recv(1024).decode("utf-8")
    info = "Hello {0}. Send private messages with /pm [person] [message]".format(name)
    client_server.send(bytes(info,"utf-8"))
    clientAddress[client_server] = name
    while True:
        msg = client_server.recv(1024)   
        if bytes("/pm","utf-8") in msg:                     #private messages        
            client = msg.decode("utf-8").split()[1]
            pm_msg = msg[5+len(client):]
            for i in clientAddress:
                if clientAddress[i] == client:
                    i.send(bytes(name+"(pm): ","utf-8")+pm_msg)
                    print(name+" send private message to "+client)
                               
        elif msg != bytes("exit", "utf-8"):                  #messages
            for i in clientAddress:
                if i != client_server:                    
                    i.send(bytes(name+": ","utf-8")+msg)
                    print(name+" send message to all")
       
        else:                                               #exiting chat room
            client_server.close()
            del clientAddress[client_server]
            for i in clientAddress:
                i.send(bytes("{0} has left the chat room.".format(name),"utf-8"))
            
            print("{0} has logged out.".format(address))
            break

def start():
    while True:
        client_socket, address = server.accept()
        print("{0} Connected".format(address))
        client_socket.send(bytes("Your Username:","utf-8"))
        Thread(target=messages, args=(client_socket,address)).start()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen(5)
thr = Thread(target=start)
thr.start()
