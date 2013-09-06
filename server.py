#!/usr/bin/python

import socket

# This creates a socket and instatiates the variable "tcpSocket" with the socket object
# socket.AF_INET is standard used called the address family -- its always this value for internet based apps
# socket.SOCK_STREAM is the type of socket you are creating, this creates a TCP socket, socket.SOCK_DATAGRAM would be used for UDP
tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# This calls the setsockopt() method which allows the server to reuse the server socket object (IP addr and port combo) quickly 
# Without this line you would have to wait for the OS to free the socket would could take mins
tcpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

# Here is where we would actually bind that raw socket we just created to an address and a port using the bind() method
# The two arguments are passed in as a Tuple
tcpSocket.bind(("0.0.0.0", 8000))

# Now that we have a fully created socket we want to have the socket listen on that port.  
# The listen() method is used to accomplish this - The single argument is the number of connections it can handle at once 
tcpSocket.listen(2)

print "Waiting for a Client...."

# Now this is setup to handle a connection from a client
# The accept() returns a tuple this will handle the creation of a client socket when a client connects to the server
# When a client connects to the server the accept() method will create the variables "client", "ip" and "port"
# The "client" variable will contain the client socket object created by the accept() method.
# The "ip" and "port" variables will contain the values of the client's IP and the remote port of the client
(client, (ip, port)) = tcpSocket.accept()

# The accept() method will wait for a connection and then once a connection happens it will execute the rest of the code
# Here we use the "ip" variable populated by the accept() method to print the statement below:
print " Received connection from : ", ip

# Here we simple print this output
print"Starting ECHO output...."

# A variable is populated with some data so the while loop executes
data = 'any key'

# Here a while loop is created to basically check "Is there data in the "data" variable?"  
# If there is a length is true or not -1 then the body of the while loop is executed
while len(data) :

# Inside the while loop we set the variable data to the value recieved by the client using recv() method
# The value 2048 is the amount of data that the server will receive 
# This uses the variable created by the accept() method "client" with the method recv()
	data=client.recv(2048)
# Here we print out the data that the client sent to the server
	print "Client sent: ",data
# Here we simply send the data back to the client.  We could put anything here, but we are just echo'n what they send
	client.send(data)

# Now we are outside of the while loop, this condition would only be executed if the client closes the connection:
print "Closing connection..."
# We close the client side socket object which was created by the accept() method
client.close()

# Now we cloes the server side socket object which was created by the socket.socket() method
print "Shutting down the server..."
tcpSocket.close()
