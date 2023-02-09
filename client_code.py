
import socket
import threading

HOST = "127.0.0.1"  
PORT = 65432  

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
print(f"[CONNECTED] Client connected to server at {HOST}:{PORT}")
name = input("enter the name of client : ")
client.send(name.encode("utf-8"))

def sender():
    while True:
        message=input()
        client.sendall(message.encode("utf-8"))

def receiver():
    while True:
        receiving_message = client.recv(1024)
        if receiving_message:
            message=receiving_message.decode()
            print(message)

sender_thread = threading.Thread(target=sender)
receiver_thread = threading.Thread(target=receiver)

sender_thread.start()
receiver_thread.start()

sender_thread.join()
receiver_thread.join()
