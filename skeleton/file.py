#! /usr/bin/env python3 

import re



texto = '''
user:[Administrator] rid:[0x1f4]
user:[Guest] rid:[0x1f5]
user:[krbtgt] rid:[0x1f6]
user:[DefaultAccount] rid:[0x1f7]
user:[ryan] rid:[0x451]
user:[marko] rid:[0x457]
user:[sunita] rid:[0x19c9]
user:[abigail] rid:[0x19ca]
user:[marcus] rid:[0x19cb]
user:[sally] rid:[0x19cc]
user:[fred] rid:[0x19cd]
user:[angela] rid:[0x19ce]
user:[felicia] rid:[0x19cf]
user:[gustavo] rid:[0x19d0]
user:[ulf] rid:[0x19d1]
user:[stevie] rid:[0x19d2]
user:[claire] rid:[0x19d3]
user:[paulo] rid:[0x19d4]
user:[steve] rid:[0x19d5]
user:[annette] rid:[0x19d6]
user:[annika] rid:[0x19d7]
user:[per] rid:[0x19d8]
user:[claude] rid:[0x19d9]
user:[melanie] rid:[0x2775]
user:[zach] rid:[0x2776]
user:[simon] rid:[0x2777]
user:[naoki] rid:[0x2778]
'''

#padrao = re.compile(r'\[[a-zA-Z]*\]')
#check = str(padrao.findall(texto))
#print(check[1:-1])

#f = open("users.txt","r")
#g = open("users2.txt", "w")



#print(f.readline())

#for x in f:
#    g.write(x) 
#    g = open("users2.txt", "r")
#    print(g.read())

def arqExiste(nome):
   try:
      a = open(nome, "rt")
      a.close()
    except FileNotFoundError:
        return False
    else:
        return True

arq = "users-regex.txt"

if arqExiste():