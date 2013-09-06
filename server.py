#!/usr/bin/python

import socket

# This creates a socket and instatiates the variable "tcpSocket" with the socket object
tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# This calls the setsockopt() method which allows the server to reuse the server socket object (IP addr and port combo) quickly 
tcpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
# Here is where we would actually bind that raw socket we just created to an address and a port using the bind() method
tcpSocket.bind(("0.0.0.0", 8000))
# The listen() method is used to accomplish this - The single argument is the number of connections it can handle at once 
tcpSocket.listen(2)
print "Waiting for a Client...."
# When a client connects to the server the accept() method will create the variables "client", "ip" and "port"
# The "client" variable will contain the client socket object created by the accept() method.
# The "ip" and "port" variables will contain the values of the client's IP and the remote port of the client
(client, (ip, port)) = tcpSocket.accept()
print " Received connection from : ", ip
print"Starting ECHO output...."

# A variable is populated with some data so the while loop executes
data = 'any key'
# Here a while loop is created to basically check "Is there data in the "data" variable?"  
# If there is a length is true or not -1 then the body of the while loop is executed
while len(data) :
# Inside the while loop we set the variable data to the value recieved by the client using recv() method
	data=client.recv(2048)
# Here we print out the data that the client sent to the server
	print "Client sent: ",data
# Here we simply send the data back to the client.  We could put anything here, but we are just echo'n what they send
	client.send(data)
# Now we are outside of the while loop, this condition would only be executed if the client closes the connection:
print "Closing connection..."
# We close the client side socket object which was created by the accept() method
client.close()

# Close the server side socket object which was created by the socket.socket() method
print "Shutting down the server..."
tcpSocket.close()
