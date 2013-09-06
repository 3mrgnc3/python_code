#!/usr/bin/python

import SocketServer, sys

# Creating a class that must be a subcalss of the BaseRequestHandler (this is req. of the SocketServer package)
class EchoHandler(SocketServer.BaseRequestHandler) :

# Creates a method to handle connections coming in to the server
	def handle(self):

# The self.client_address contains all of the client details populated by the SocketServer package
		print "Connection from: ", self.client_address
# This creates a variable with some data in it so the while loop will execute initially 
		data = 'anyData'
		
# While there is a length to data execute the body
		while len(data):
# Data is set to the .request.recv() method which is basically what the server will rec. from a client connection
			data = self.request.recv(1024)
			print "Client sent the following: \n", data
# Here we use the request.send() method to send data to the client
# This could be anything, so if you are analyzing malware you could change this to send back what the malware asked for
# It's possible you may learn more about the malware's behavior this way
			self.request.send(data)
# This executes outside the body of the while loop, which only means the connection is closed
		print "Connection closed"

# Here we setup a variable which will contain a tuple of the IP ("0.0.0.0" means listen on all addresses)
# and it takes in an argument from the CLI for the port
serverAddr = ("0.0.0.0", int(sys.argv[1]))
print "Server started, waiting for a connection...."
# Tells the SocketServer to invoke the TCPServer() method - this takes two arguments
# 1st argument is a tuple which contains the IP/Port information, which we made with serverAddr variable
# The second argument is a Class which will be used to handle connections to the server.
# This was the class we created earlier in the code
server = SocketServer.TCPServer(serverAddr, EchoHandler)

# This is added to have the TCPServer process as many clients as possible
# You could use another method to handle single connections, but that is really never used
server.serve_forever()
