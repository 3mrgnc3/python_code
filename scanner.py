#!/usr/bin/python

import socket

def retBanner(ip, port):

  try:

    socket.setdefaulttimeout(2)
    s = socket.socket()
    s.connect((ip, port))
    s.send('h@x0r\r\n')
    banner = s.recv(1024)
    return banner

  except:
    return

def main():
  portList = [21, 23, 22, 25, 110, 53, 80, 443, 8000, 137, 138, 139, 445]
  for x in range(200, 255):
    ip = '192.168.13.' + str(x)
    for port in portList:
      banner = retBanner(ip, port)
      if banner:
        prt = str(port)
        print '[+] ' + ip + ':'+ prt + ' ' + banner

if __name__ == '__main__':
  main()
