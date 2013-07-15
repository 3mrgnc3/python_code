#!/usr/bin/env python
import sys, optparse, socket, datetime


def checkPI(target, port):
	try:
		socket.setdefaulttimeout(7)
		s = socket.socket()
		s.connect((target, int(port)))
		s1 = "\x00" * 0x100
		s.sendall(s1)
		data = s.recv(0x100)
		if len(data) != 0x100:
			s.close()
			return
		data = s.recv(0x4)
		s.close()
		if data != "\xD0\x15\x00\x00":
			return
		print "%s Poison %s:%s" % (datetime.datetime.now(), target, port)
		
	except socket.timeout as e:
		pass
	except socket.error as e:
		pass


def main():
  	parser = optparse.OptionParser('usage%prog '+\
    		'-t <target> -p <port>')
  	parser.add_option('-t', dest='target', type='string', \
    		help='specify target IP')
  	parser.add_option('-p', dest='port', type='string', \
    		help='specify target port')
  	(options, args) = parser.parse_args()
  	target = options.target
  	port = options.port

	if (target == None) or (port == None):
		print parser.usage()
		sys.exit()

	else:
		checkPI(target, port)


if __name__ == "__main__":
      main()

