#################################################################################
#	iptrap.py - Auto add iptables rules based on connections		#
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
			os.system("sudo iptables -A INPUT -p tcp -s "+RHOST+"  -j DROP")
			print "Added the following rule: iptables -A INPUT -p tcp -s "+RHOST+" -j DROP"
		elif RHOST in WLIST:
			print "Connection from white listed IP: "+RHOST


def ipflush():
	print "Removed the following entries:"
	os.system("sudo iptables -L | grep 'DROP'")
	os.system("sudo iptables --flush")


def iplist():
	os.system("sudo iptables -L | grep 'DROP'")


def main():
	parser = optparse.OptionParser(sys.argv[0] +\
     	' -p <Port_Num> -f <flush_rules> -l <list_rules> -w <white_list>')
	parser.add_option('-p', dest='LPORT', type='int', \
	help ='specify a port to listen on')
	parser.add_option('-f', action="store_true", dest='flush', \
	help='This flushes the current iptables rules', default=False)
	parser.add_option('-l', action="store_true", dest='list', \
        help='List the current rules that were added', default=False)
	parser.add_option('-w', dest='WLIST', type='string', \
	help='specify an ip or comma separated IPs to whitelist ip,ip,ip,etc.')
   	(options, args) = parser.parse_args()
	LPORT = options.LPORT
	flush = options.flush
	list = options.list
	global WLIST
	WLIST = options.WLIST
	if WLIST == None:
		WLIST=''

	if (LPORT == None) & (flush == False) & (list == False):
		print parser.usage
		sys.exit(0)

	if (flush == False) & (list == False):
		listen(LPORT)
	
	if flush == True:
		ipflush()

	if list == True:
		iplist()


if __name__=="__main__":
	main()
