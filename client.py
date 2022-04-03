from dateutil import parser
import threading
import datetime
import socket
import time

# send time from client side
def sendTime(client):
    while True:
        client.send(str(datetime.datetime.now()).encode())
        print("time sent successfully \n")
        time.sleep(5)

# Receive synced time
def ReceiveTime(client):
    while True:
        Synchronized_time = parser.parse(client.recv(1024).decode())
        print("Synchronized time at the client is: " + str(Synchronized_time), end="\n\n")

def startClient(port=8080):
    client = socket.socket()
    client.connect(('127.0.0.1', port))

    print("Sending time to server\n")
    send_thread = threading.Thread(
        target=sendTime,
        args=(client,))
    send_thread.start()

    print("Receiving synchronized time from server\n")
    receive_thread = threading.Thread(
        target=ReceiveTime,
        args=(client,))
    receive_thread.start()


if __name__ == '__main__':
    startClient(port=8080)
