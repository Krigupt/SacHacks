import socket
import threading

host = '127.0.0.1'
port = 55545

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

users = []
nicknames = []

def broadcast(message):
    for user in users:
        user.send(message)


# Handling Messages From users
def handle(user):
    while True:
        try:
            # Broadcasting Messages
            message = user.recv(1024)
            broadcast(message)
        except:
            # Removing And Closing users
            index = users.index(user)
            users.remove(user)
            user.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break


def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        users.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()