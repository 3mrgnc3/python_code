#!/usr/bin/python

import socket, sys

if len(sys.argv) != 3:

	print "Usage: <script>.py <mail server> <username file>"
	sys.exit(0)

server=sys.argv[1]
efile=sys.argv[2]
# Create a socket
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the Server
connect=s.connect((server, 25))

# Recieve and print the banner
banner=s.recv(1024)

# Send a VRFY Request to the server and print the result

fdesc=open(efile, "r")

for name in fdesc:
	s.send('VRFY ' + name + '\r\n')
	result=s.recv(1024)
	print result

# Close socket
s.close()
