from _winreg import *
from optparse import OptionParser
import sys

def regfor(): # Work in Progress, need to add more keys 
    print " ### Software\Microsoft\Windows\CurrentVersion\Run Entries ##"
    run = "Software\Microsoft\Windows\CurrentVersion\Run"
    key = OpenKey(HKEY_LOCAL_MACHINE, run)
    try:
        i = 0
        while True:
            subkey = EnumValue(key, i)
            print subkey
            i += 1
    except WindowsError:
        pass


def main():
    parser = OptionParser('%prog '+\
        '-f <reg>')
    parser.add_option('-r', dest='regf', type='string', \
        help='dump forensic artifacts from the reg')
    (options, args) = parser.parse_args()
    regf = options.regf
    if regf == None:
        print parser.usage
        sys.exit(0)

    if regf != None:
        regfor()
        # Add a function to check File System



if __name__ == "__main__":
      main()
