#!/usr/bin/env python

import optparse, dns.resolver, dns.zone, dns.query, dns.reversename, sys


def lookup(lhost, ltype):
	# Set this to the file that you want to contain your DNS server 'nameserver 8.8.8.8' to use Google
	resolver = dns.resolver.Resolver(filename='./resolv.conf')
	# Mail Server
	if ltype == 'MX':
  		answers = dns.resolver.query(lhost, ltype)
  		for rdata in answers:
    			print 'host', rdata.exchange, 'has preference', rdata.preference
	# Host A or AAAA
	elif (ltype == 'A') | (ltype == 'AAAA'):
		answers = dns.resolver.query(lhost, ltype)
  		for rdata in answers:			    
			print rdata.address
	# Name Server
	elif ltype == 'NS':
		answers = dns.resolver.query(lhost, ltype)
		for rdata in answers:
			print rdata.to_text()
	# IP to Domain Lookup
	elif ltype == 'reverse':
		print dns.reversename.from_address(lhost)
	# Zone Transfer
	elif ltype == 'xfr':
		aws = dns.resolver.query(lhost, 'NS')
		for rdata in aws:
			ns = str(rdata)
			try:
      				zone = dns.zone.from_xfr(dns.query.xfr(ns, lhost))
      				names = zone.nodes.keys()
      				names.sort()
      				for ns in names:
        				print zone[ns].to_text(ns)

    			except:
      				pass

def main():
	parser = optparse.OptionParser(sys.argv[0]+' '+\
		'-r <domain||IP> -t <record type:A, MX, NS, AAAA, reverse, xfr>')
	parser.add_option('-r', dest='lhost', type='string', \
		help='Specify a host by IP or domain to lookup')
	parser.add_option('-t', dest='ltype', type='string', \
		help='Specify a host by IP or domain to lookup')
	(options, args) = parser.parse_args()
	if (options.lhost == None) & (options.ltype == None):
		print parser.usage
		sys.exit(0)

	lhost = options.lhost
	ltype = options.ltype

	lookup(lhost, ltype)


if __name__ == "__main__":
      main()
