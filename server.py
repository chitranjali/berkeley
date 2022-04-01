import socket
import threading

''' thread t receives several clients and starts receiving time '''
def fetchTime(server):
    # get clock time for each connected client
    while True:
        client_connector, addr = server.accept()
        client_address = str(addr[0]) + ":" + str(addr[1])

        print(client_address + " succesfully connected to client")

        client_thread = threading.Thread(
            target = startReceivingClockTime,
            args = (client_connector,
                    client_address, ))
        client_thread.start()

# this will start our server to listen to clients
def startServer(port = 8080):
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET,
                             socket.SO_REUSEADDR, 1)
    server.bind(('', port))
    server.listen(7)
    print("Started server \n")
    t = threading.Thread(
        target=fetchTime,
        args=(server,))
    t.start()


# main function
if __name__ == '__main__':
    # Trigger the Clock Server
    startServer(port = 8080)