#!/usr/bin/env python

import optparse, base64, string, sys


def decode(estring):

	default_B64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

	if cust_B64 != None:
		estring = estring.translate(string.maketrans(cust_B64, default_B64))
		decoded_str = base64.b64decode(estring)
		print decoded_str
	else:
		decoded_str = base64.b64decode(estring)
		print decoded_str

def main():
        parser = optparse.OptionParser(sys.argv[0]+' '+\
                '-s <encoded_str> OR -c <custom_alpha>')
        parser.add_option('-s', dest='estring', type='string', \
                help='specify b64encoded string')
        parser.add_option('-c', dest='cust', type='string', \
                help='specify custom b64 alpha')
        (options, args) = parser.parse_args()
        if (options.cust == None) & (options.estring == None):
                print parser.usage
                sys.exit(0)	
	global cust_B64
	cust_B64 = options.cust
	estring = options.estring
	decode(estring)

if __name__ == "__main__":
      main()
