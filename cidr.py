#!/usr/bin/env python
import sys, os, optparse
from cymruwhois import Client


def look(ip):
	try:
		c=Client()
		ipvar = ip.rsplit()
		ipv = ipvar[0]
		r=c.lookup(ip)
        	net = r.prefix
        	owner = r.owner
        	cc = r.cc
        	line = 'and not net %-20s # - %15s (%s) - %s' % (net,ipv,cc,owner)
        	mem.append(line)

	except:
		print "Lookup failed for: "+ip.strip()

def uniq(mem):
	for item in mem:
                cidr = item.split()[3]
                if cidr in temp:
                        continue
                else:
                        temp.append(cidr)
                        print item

def checkFile(cfile):
        if not os.path.isfile(cfile):
                print '[-] ' + cfile + ' does not exist.'
                sys.exit(0)

        if not os.access(cfile, os.R_OK):
                print '[-] ' + cfile + ' access denied.'
                sys.exit(0)

        print '[+] Querying from:  ' +cfile

def main():
        parser = optparse.OptionParser('%prog '+\
        '-r <file_with IPs>')
        parser.add_option('-r', dest='ips', type='string', \
                help='specify target file with ips')
        (options, args) = parser.parse_args()
        ips = options.ips
	global temp 
	temp = []
	global mem
	mem = []

        if (ips == None):
                print parser.usage
                sys.exit(0)

        if ips != None:
		checkFile(ips)
        	F = ips
        	ipF = open(F,'r')
        	for line in ipF:
                	look(line)
		uniq(mem)

if __name__ == "__main__":
      main()

