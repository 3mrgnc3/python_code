#!/usr/bin/env python

import dpkt
import socket
import sys
import optparse
import re
import os

# Function to decode HTTP packet
def httpGET(pcap):
	for (ts, buf) in pcap:
		try:
			eth = dpkt.ethernet.Ethernet(buf)
      			ip = eth.data
      			src = socket.inet_ntoa(ip.src)
      			dst = socket.inet_ntoa(ip.dst)
      			tcp = ip.data
      			http = dpkt.http.Request(tcp.data)
      			req = http.method
      			host = http.headers['host']
      			if http.method == 'GET':
        			uri = http.uri.lower()
				line = '%20s -> %-20s  %s %s%s' % (src,dst,req,host,uri)
        			print line

    		except:
      			pass

# Function to decode HTTP packets and focus on the UA
def httpUA(pcap):
        for (ts, buf) in pcap:
                try:
                        eth = dpkt.ethernet.Ethernet(buf)
                        ip = eth.data
                        src = socket.inet_ntoa(ip.src)
                        dst = socket.inet_ntoa(ip.dst)
                        tcp = ip.data
                        http = dpkt.http.Request(tcp.data)
                        req = http.method
                        ua = http.headers['user-agent']
                        host = http.headers['host']
                        if http.method == 'GET':
                                uri = http.uri.lower()
                                line = '%20s -> %-20s  %-30s %s' % (src,dst,host,ua)
                                print line

                except:
                        pass

###################################
# Prints small HTTP packets	  #
# GET with 2 or less other fields #
###################################
def smallHTTP(pcap):
        for (ts, buf) in pcap:
                try:
                        eth = dpkt.ethernet.Ethernet(buf)
                        ip = eth.data
                        src = socket.inet_ntoa(ip.src)
                        dst = socket.inet_ntoa(ip.dst)
                        tcp = ip.data
                        http = dpkt.http.Request(tcp.data)
			req = http.method
			uri = http.uri.lower()
                        if len(http.headers) < 3:
				line = '%20s -> %-20s  %s  %s' % (src,dst,req,uri)
				a = []
				b =[]
				for items in http.headers:
					a.append(items)
                                for item in a:
					f = http.headers[item]
					b.append(f)
				if len(b) == 2:
					print line + "   " + b[0] + "    " + b[1]
				elif len(b) == 1:
					print line + "   " + b[0]
				else:
					print line

                except:
                        pass


###########################
# Function to check file  #
###########################
def checkFile(cfile):
	if not os.path.isfile(cfile):
                print '[-] ' + cfile + ' does not exist.'
                sys.exit(0)

        if not os.access(cfile, os.R_OK):
                print '[-] ' + cfile + ' access denied.'
                sys.exit(0)

        print '[+] Parsing pcap from:  ' +cfile



def main():
  

###########################################
# Usage: ./decoder.py -d <docoder> <pcap> #
###########################################

###########################################
# Check for proper arguments and switches #
###########################################
        parser = optparse.OptionParser(sys.argv[0] +' '+\
                '-d <decoder> <pcap file>')
        parser.add_option('-d', dest='decoder', type='string', \
                help='specify a decoder to use: HTTP or UA')
        (options, args) = parser.parse_args()
        decoder = options.decoder

        if (decoder == None) or sys.argv <3:
                print parser.usage
                sys.exit(0)

        decoders = "HTTP, UA, small"

	if decoder == 'list':
                print 'Current decoders are: '+decoders
		sys.exit(0)

	pcapf = sys.argv[3]
	checkFile(pcapf)
	f = open(pcapf)
	pcap = dpkt.pcap.Reader(f)


# Prints Src --> Dst HOST/GET_REQUEST
	if decoder == 'HTTP':
		httpGET(pcap)

# Prints Src --> Dst Host_field UA
	if decoder == 'UA':
		httpUA(pcap)

# Prints HTTP packets that have less than 3 fields after the IP/Request	
	if decoder == 'small':
		smallHTTP(pcap)

if __name__ == "__main__":
        main()
