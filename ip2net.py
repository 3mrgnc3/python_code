#################################################################################
#	ip2net.py -- Looks up network information given a file containing IPs   #
#       Heavily commented for educational purposes                              #
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

#!/usr/bin/env python
import sys, os, optparse
from cymruwhois import Client


def look(iplist):
	c=Client() # creates an instance of the Client class
	try:
		r = c.lookupmany_dict(iplist) # leverages the lookupmany_dict() function to pass in a list of IPs
		for ip in iplist: # Iterates over the ips in the list to use a key value in the returned dictionary from lookupman_dict()
			net = r[ip].prefix; owner = r[ip].owner; cc = r[ip].cc # gets the networking information from the dictionary
			line = '%-20s # - %15s (%s) - %s' % (ip,net,cc,owner) # formats the line to print cleanly
        		print line
	except:pass

def checkFile(ips): # Checks to ensure the file can be read
        if not os.path.isfile(ips):
                print '[-] ' + ips + ' does not exist.'
                sys.exit(0)
        if not os.access(ips, os.R_OK):
                print '[-] ' + ips + ' access denied.'
                sys.exit(0)
        print '[+] Querying from:  ' +ips

def main():
        parser = optparse.OptionParser('%prog '+\	# Script usage
        '-r <file_with IPs>')
        parser.add_option('-r', dest='ips', type='string', \	# Creates a '-r' switch which reads in a string
                help='specify target file with ips')
        (options, args) = parser.parse_args()
        ips = options.ips # Assigns a -r <fileName> to variable 'ips'
        if (ips == None): # If not filename given it will print the script usage and exit
                print parser.usage
                sys.exit(0)
        if ips != None:	# Execute if ips has a value
		checkFile(ips)	# Execute the function to check if the file can be read
		iplist = []	# create the ipslist list object
        	for line in open(ips, 'r'): # Parse File to create a list
			iplist.append(line.strip('\n')) # Appends that line in the file to list and removes the new line char
		look(iplist)	# pass the iplist list object to the look() function

if __name__ == "__main__":
      main()

