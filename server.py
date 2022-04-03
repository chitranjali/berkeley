from dateutil import parser
import socket
import threading
import datetime
import time

client_data = {}

def getClockTime(connector, address):
    while True:
        clock_string = connector.recv(1024).decode()
        clock_time = parser.parse(clock_string)
        time_diff = datetime.datetime.now() - \
                    clock_time

        client_data[address] = {
            "clock_time": clock_time,
            "time_difference": time_diff,
            "connector"	: connector
        }

        print("Updated client data:  " + str(address),
              end="\n\n")
        time.sleep(5)

''' thread t receives several clients and starts receiving time '''
def fetchTime(server):
    # get clock time for each connected client
    while True:
        client_connector, addr = server.accept()
        client_address = str(addr[0]) + ":" + str(addr[1])

        print(client_address + " succesfully connected to client")

        client_thread = threading.Thread(
            target = getClockTime,
            args = (client_connector,
                    client_address, ))
        client_thread.start()

def getClockDiff():
    # current_client_data = client_data.copy()

    time_difference_list = list(client['time_difference']
                                for client_addr, client
                                in client_data.items())
    sum_of_clock_differences = sum(time_difference_list, datetime.timedelta(0, 0))
    avg_clock_difference = sum_of_clock_differences / len(client_data)

    return avg_clock_difference

def syncClocks():
    while True:
        print("Number of clocks being synchronized: " + \
              str(len(client_data)))

        if len(client_data) > 0:
            avg_diff = getClockDiff()

            for addr, client in client_data.items():
                try:
                    sync_time = datetime.datetime.now() + avg_diff
                    client['connector'].send(str(sync_time).encode())

                except Exception as e:
                    print("There's some exception while syncing clocks with address " + str(addr))
        else:
            print("No client data to sync")

        time.sleep(5)

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

    # synchronize all client clocks
    print("Synchrnize all clocks...\n")
    sync_t = threading.Thread(
        target=syncClocks,
        args=())
    sync_t.start()


# main function
if __name__ == '__main__':
    # Trigger the Clock Server
    startServer(port = 8080)