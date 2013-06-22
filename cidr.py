#!/usr/bin/env python2.7
import sys
import os
import optparse
from cymruwhois import Client


def look(ip):
	try:
        	c=Client()
		i = ip.strip()
		ii = str(i[0])
        	r=c.lookup(ii)
        	net = r.prefix
        	owner = r.owner
        	cc = r.cc
        	line = '%-20s # - %15s:%5s -  %s %s' % (net,ii,owner,cc)
        	print line

	except:
		pass


def checkFile(cfile):
        if not os.path.isfile(cfile):
                print '[-] ' + cfile + ' does not exist.'
                sys.exit(0)

        if not os.access(cfile, os.R_OK):
                print '[-] ' + cfile + ' access denied.'
                sys.exit(0)

        print '[+] Querying from:  ' +cfile



def main():

        parser = optparse.OptionParser('usage%prog '+\
        '-r <file_with domains>')
        parser.add_option('-r', dest='domains', type='string', \
                help='specify target file with domains')
        (options, args) = parser.parse_args()
        domains = options.domains

        if (domains == None):
                print parser.usage
                sys.exit(0)

        checkFile(sys.argv[2])

        if domains != None:
                F = sys.argv[2]
                ipF = open(F,'r')
                for line in ipF:
                        look(line)


if __name__ == "__main__":
      main()

