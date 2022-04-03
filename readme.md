**Berkely's Algorithmn**

**Working:**

* A node is acted as a master, and here we are taking
3 clients to synchronize the clocks.

* The master deamon(server.py) starts and starts accepting clients
and receiving their clock times.

* Then the master calculates the average time among all the co
connected clients and sends the corresponding time to
all the clients. This all is done parallelly using threads.

* After the synchronization, each process prints out its logical
clock to check the result of synchronization.

