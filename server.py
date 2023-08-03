import socket
import threading

HOST = '127.0.0.1'
PORT = 1234 #YOU can use any port between 0 to 65535
LISTNER_LIMIT =5
active_clients = [] #list of all active currently connected users

# function to listen for upcoming messeages from the client
def listen_for_messages(client,username):
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            final_msg = username + '~' + message
            send_message_to_all(final_msg)
        else:
            print(f"the message send from client {username} is empty")

def client_handler(client):
    # server will listen for client message that will contain the username
    while 1:
        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username,client))
            promt_msg = "SERVER~ "+f"{username} added to the chat"
            send_message_to_all(promt_msg)
            break
        else:
            print("client username is empty")
    threading.Thread(target=listen_for_messages,args=(client,username, )).start()

# function to send message to a single client
def send_message_to_client(client,message):
    client.sendall(message.encode('utf-8'))


# function to send any new msg to all the clients that are currently conneted to the server
def send_message_to_all(message):
    for user in active_clients:
        send_message_to_client(user[1],message)

def main():
    # creating the socket class object
    #AF_INET : we are going to use IPv4 addresses
    # SOCK_STREAM = TCP, SOCK_DGRAM  = UDP
    server  = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    #creating a try catch block
    try:
        # provide the server with an address in the form of host ip and port
        server.bind((HOST,PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to bind to host  {HOST} and port {PORT}")

    # set server limit
    server.listen(LISTNER_LIMIT)

    #this loop will keep listening to client connections
    while 1:
        client, address = server.accept()
        print(f"successfully connected to client {address[0]}  {address[1]}")

        threading.Thread(target=client_handler,args=(client, )).start()

    
    


if __name__ == '__main__':
    main()