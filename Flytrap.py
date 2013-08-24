#################################################################################
#	Flytrap.py - Auto add iptables rules based on connections		#
#	Copyrighted:  Primal Security Podcast - www.primalsecurity.net         	#
#									       	#
#    	This program is free software: you can redistribute it and/or modify	#
#    	it under the terms of the GNU General Public License as published by	#
#    	the Free Software Foundation, either version 3 of the License, or	#
#    	(at your option) any later version.					#
#										#
#    	This program is distributed in the hope that it will be useful,		#
#    	but WITHOUT ANY WARRANTY; without even the implied warranty of		#
#    	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the		#
#    	GNU General Public License for more details.				#
#										#
#    	You should have received a copy of the GNU General Public License	#
#    	along with this program.  If not, see <http://www.gnu.org/licenses/>.	#
#################################################################################

import socket, os, optparse, sys


def listen(LPORT):	
	tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
	tcpSocket.bind(('0.0.0.0', int(LPORT)))
	tcpSocket.listen(10)

	print "Listening on 0.0.0.0:"+str(LPORT)
	while 1:
		(client, (RHOST, RPORT)) = tcpSocket.accept()
		print "Received connection from : ", RHOST
		if RHOST not in WLIST:
			randomNum=str(random.randrange(1, 1000000))
			command="netsh advfirewall firewall add rule name=\"BAN"+randomNum+"\" protocol=TCP action=block dir=IN remoteip="+host
			print command
			os.system(command)

		elif RHOST in WLIST:
			print "Connection from white listed IP: "+RHOST


def main():
	parser = optparse.OptionParser(sys.argv[0] +\
     	' -p <Port_Num> optional -w <white_list>')
	parser.add_option('-p', dest='LPORT', type='int', \
	help ='specify a port to listen on')
	parser.add_option('-w', dest='WLIST', type='string', \
	help='specify an ip or comma separated IPs to whitelist ip,ip,ip,etc.')
   	(options, args) = parser.parse_args()
	LPORT = options.LPORT
	global WLIST
	WLIST = options.WLIST
	if WLIST == None:
		WLIST=''

	if (LPORT == None):
		print parser.usage
		sys.exit(0)

	listen(LPORT)

if __name__=="__main__":
	main()
