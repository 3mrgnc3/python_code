#################################################################################
#	Gumdrop.py - Windows Recon -- for Incident Response or Cyber comps	#
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

from _winreg import *
from optparse import OptionParser
import sys, os, subprocess

def regfor(): # Work in Progress, need to add more keys
    proc = subprocess.Popen(["hostname"], stdout=subprocess.PIPE, shell=True)
    (name, er) = proc.communicate()
    report.write("Forensic Report for Host: "+name)
    report.write("\n")
    report.write("[+] HKLM\Software\Microsoft\Windows\CurrentVersion\Run Entries ")
    report.write("\n")
    run = "Software\Microsoft\Windows\CurrentVersion\Run"
    key = OpenKey(HKEY_LOCAL_MACHINE, run)
    try:
        i = 0
        while True:
            subkey = EnumValue(key, i)
            report.write(subkey[0]+": "+subkey[1].strip("\""))
            report.write("\n")
            i += 1
    except WindowsError:
        pass

def ffor(): # Add additional checks
    report.write("\n")
    report.write("[+] Displaying Network Interface Information via ipconfig:")
    ipconfig = subprocess.Popen(["ipconfig", "/all"], stdout=subprocess.PIPE, shell=True)
    (i, e) = ipconfig.communicate()
    report.write(i)
    report.write("\n")
    report.write("\n")
    report.write("[+] Listing %TEMP% Directory ")
    report.write("\n")
    proc = subprocess.Popen(["dir", "/b", "%TEMP%"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    report.write(out)
    report.write("\n")
    report.write("\n")
    report.write("[+] Listing STARTUP Folder ")
    startup = subprocess.Popen(["dir", "/b", "%UserProfile%\Start Menu\Programs\StartUp"], stdout=subprocess.PIPE, shell=True)
    (out, err) = startup.communicate()
    report.write(out)
    report.write("\n")
    report.write("\n")
    report.write("[+] Listing ARP Entries -- What can I talk to?")
    arp = subprocess.Popen(["arp", "-a"], stdout=subprocess.PIPE, shell=True)
    (o, e) = arp.communicate()
    report.write(o)
    report.write("\n")
    report.write("\n")
    report.write("[+] Displaying ESTABLISHED Connections:"+"\n")
    proc = subprocess.Popen(["netstat", "-ano", "|", "findstr", "ESTABLISHED"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    report.write("[+] Displaying LISTENING Connections:"+"\n")
    proc = subprocess.Popen(["netstat", "-ano", "|", "findstr", "LISTENING"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    report.write(out)
    report.write("\n")
    report.write("\n")
    report.write("[+] Displaying Running Processes:"+"\n")
    proc = subprocess.Popen(["tasklist"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    report.write(out)
    report.write("\n")
    report.write("\n")
    report.write("[+] Displaying Environment Variables:"+"\n")
    proc = subprocess.Popen(["set"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    report.write(out)
                
    
def main():
    parser = OptionParser('%prog '+\
        '-w <reportName>')
    parser.add_option('-w', dest='rep', type='string', \
        help='Name for report')
    (options, args) = parser.parse_args()
    rep = options.rep
    global report
    report = open(rep, 'w')

    if rep == None:
        print parser.usage
        sys.exit(0)
    if rep != None:
        regfor()
        ffor()
        report.close()

if __name__ == "__main__":
      main()
