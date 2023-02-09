import socket
import threading
from typing import NamedTuple

HOST = "127.0.0.1"  
PORT = 65432  
ADDR = (HOST,PORT)
LOST="Lost it's Connection"
DISCONNECT = "is disconnected."
HELP=("The list of help commands are below:/n"
'''/help-To print out a list of all supported commands and their behaviors.
/users-To request a list of users from the server and then print out their names.
/dm username "message" -To send the message between quotes to the specified user. The client will make the request to the server.
/bc "message" -To send the message between quotes to all other connected users. The client will make the request to the server.
/quit - Disconnect from the server. Before disconnecting, send a message to the server saying you will disconnect.''')
connections={}
names={}
def receive_connections(addr: str,client: str):
    connections[addr] = client

def broadcast(data: str, name: str):
    for i in names:
        names[i].sendall(f"{name}: {data[5:-1]}".encode("utf-8"))

def connection_closing(addr: str,client: str,name: str):
    try:
        print("Active Users List changed.")
        pop_user=name
        names.pop(f'{pop_user}')
    except ConnectionResetError as e:
        print("code erroring!!!!!!!!!!!!")


def quitting(addr: str,client: str, name: str,server: str):
    for i in names:
        names[i].sendall(f"{name} {DISCONNECT}".encode("utf-8"))
    connection_closing(addr,client,name)
    print(f"{name} is Disconnected.")
    exit()

 
def lost1(addr: str, client: str, name: str):
    try:
        connection_closing(addr,client,name)
        for i in names:
            names[i].sendall(f"[CONNECTION LOST]{name} {LOST}".encode("utf-8"))
        
    except ConnectionResetError as e:
        print(f"[CONNECTION LOST] {name} lost it's connection.")
            

def handle_client(client: str, addr: str,server: str):
    name = client.recv(1024).decode("utf-8")
    print(f"[New Connection]{name} {addr} established and connected.")
    receive_connections(addr,client)
    while True:
        if client not in names:
           names[name] = client

        with client:
            try:
                while True:
                    data= client.recv(1024).decode("utf-8")
                    data_array= data.split()
                    if data =="/help":
                        client.sendall(f"Received from server: {HELP}".encode("utf-8"))
                    elif data=="/users":
                        user_names=list(names.keys())
                        client.sendall(f"{user_names}".encode("utf-8"))
                    elif data_array[0] == "/bc":
                        broadcast(data,name)

                    elif data_array[0]=="/dm":
                        if data_array[1] in names: 
                            for i in names:
                                if data_array[1]==i:
                                    cli=names[i]
                                    a=data_array[2:]
                                    bi=" ".join(a)
                                    ci=bi[1:-1]
                                    cli.sendall(f"{name}: {ci}".encode("utf-8"))
                        else:
                            client.sendall(f"server: User '{data_array[1]}' is not connected to the server.".encode("utf-8"))

                    elif data =="/quit":
                        quitting(addr,client,name,server)
                              
                    else:
                        client.sendall(f"Message Received and Echoed: {data}".encode("utf-8"))
                    print(f"Received from {name}:",data)
            except ConnectionResetError as e:
               print(f"[CONNECTION LOST] {name} lost it's connection.")
               lost1(addr,client,name)
               break
                
                   

def main():
    print("[starting] Server is starting.....")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[Listening] Server is listening on {HOST}:{PORT}")
    while True:
        client, addr = server.accept()
        
        thread = threading.Thread(target=handle_client,args=(client,addr,server))
        thread.start()
        print(f"[Number of Active clients:] {threading.active_count() -1}")    

if __name__ == "__main__":
    main()


