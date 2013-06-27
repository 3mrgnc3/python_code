#!/usr/bin/env python

import os, urllib, sys, optparse, re

def lookup(ip):
	if domain != None:
		httpR = urllib.urlopen("http://top.robtex.com/"+domain+".html")
		out = httpR.readlines()
		for line in out:
			if 'ip.robtex.com' in line:
				if 'The IP number' in line:
					res = line.replace("</div><div class=\"dd\"><h3>", "").replace("</h3><p class=\"pp\">", "")
					match = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', res)
					if match:
						ip = match.group()
						l = '%10s	# %s' % (ip, domain)
						print l		

	elif ip != None:
		httpR = urllib.urlopen("http://ip.robtex.com/"+ip+".html")
		out = httpR.readlines()
		for line in out:
			if "meta name" in line and 'description' in line:
				print line.split("=\"")[2].replace("...\" />", "").split("\n")[0]



def main():
	parser = optparse.OptionParser(sys.argv[0]+' '+\
                '-d <domain> OR -i <ip_addr>')
        parser.add_option('-d', dest='domain', type='string', \
                help='specify target domain')
        parser.add_option('-i', dest='ip', type='string', \
                help='specify target ip')
        (options, args) = parser.parse_args()
	if (options.domain == None) & (options.ip == None):
		print parser.usage
		sys.exit()
        global domain
	global ip
	domain = options.domain
        ip = options.ip

	if ip != None:
		lookup(ip)
	elif domain != None:
		lookup(domain)


if __name__ == "__main__":
      main()

