import socket
import threading

HOST = '127.0.0.1'
PORT = 1234 #YOU can use any port between 0 to 65535

def listen_for_messages_from_server(client):
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message!='':
            username = message.split('~')[0]
            content = message.split('~')[1]
            print(f"[{username}] {content} ")
        else:
            print("message recevied from client is empty")

def communicate_to_server(client):
    username = input("enter the username: ")
    if username!='':
        client.sendall(username.encode())
    else:
        print("username cann't be empty ")
        exit(0)
    threading.Thread(target=listen_for_messages_from_server,args=(client,)).start()
    send_message_to_server(client)

def send_message_to_server(client):
    while 1:
        message = input("message: ")
        if message!='':
            client.sendall(message.encode())
        else:
            print("empty message")
            exit(0)


def main():
    # creating the socket class object
    #AF_INET : we are going to use IPv4 addresses
    # SOCK_STREAM = TCP, SOCK_DGRAM  = UDP
    client  = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # connect to server
    try:
        client.connect((HOST,PORT))
        print("connected to server")
    except:
        print(f"Unable to connect to server {HOST} {PORT}")
    communicate_to_server(client)

    
if __name__ == '__main__':
    main()