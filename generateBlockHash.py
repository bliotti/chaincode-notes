#!/usr/bin/env python3

import json
import sys
import hashlib
import getpass
import struct
import requests
from requests.auth import HTTPBasicAuth
import binascii

print('cmd entry:', sys.argv)


def generateBlockHash(header):

     def hash256(s):
          '''two rounds of sha256'''
          return hashlib.sha256(hashlib.sha256(s).digest()).digest()

     def deal_str(big_endian):
          return bytes.fromhex(big_endian)[::-1]    # [::-1] will reverse the bytes to little-endian

     def deal_int(n):
     # < means "Little-endian"
     # L means "unsigned long"
          return struct.pack("<L", n)

     def buildblockstr(s):
          '''build the block header string'''
          v = deal_str(s['versionHex'])
          print("version:\t\t",s['versionHex'])
          pb = deal_str(s['previousblockhash'])
          print("previousblockhash:\t",s['previousblockhash'])
          mkr = deal_str(s['merkleroot'])
          print("merkleroot:\t\t",s['merkleroot'])
          t = deal_int(s['time'])
          print("time:\t\t\t",s['time'])
          b = deal_int(int(s['bits'],16))
          print("bits:\t\t\t",s['bits'])
          n = deal_int(s['nonce'])
          print("nonce:\t\t\t",s['nonce'])
          print("\nCorrected Endiness")
          print("version_fmt:\t\t", v.hex())
          print("previousblockhash_fmt:\t", pb.hex())
          print("merkleroot_fmt:\t\t", mkr.hex())
          print("time_fmt:\t\t", t.hex())
          print("bits_fmt:\t\t", b.hex())
          print("nonce_fmt:\t\t", n.hex())
                    
          return (v + pb + mkr + t + b + n)
     

     blkstr = buildblockstr(header)

     print("\nblockstr:\t\t",blkstr.hex())

     blockhash = binascii.hexlify(hash256(blkstr)[::-1])

     print("blockhash:\t\t",blockhash.decode('utf-8'))

     print("Hashes match?:\t\t",header['hash'] == blockhash.decode('utf-8'))
     
     return blockhash.decode('utf-8')

if __name__ == '__main__':
     
     header = {
     "hash": "00000000000000001e8d6829a8a21adc5d38d0a473b144b6765798e61f98bd1d",
     "confirmations": 662187,
     "height": 125552,
     "version": 1,
     "versionHex": "00000001",
     "merkleroot": "2b12fcf1b09288fcaff797d71e950e71ae42b91e8bdb2304758dfcffc2b620e3",
     "time": 1305998791,
     "mediantime": 1305995943,
     "nonce": 2504433986,
     "bits": "1a44b9f2",
     "difficulty": 244112.4877743364,
     "chainwork": "0000000000000000000000000000000000000000000000006aa84fd45b2350c9",
     "nTx": 4,
     "previousblockhash": "00000000000008a3a41b85b8b29ad444def299fee21793cd8b9e567eab02cd81",
     "nextblockhash": "0000000000001c0533ea776756cb6fdedbd952d3ab8bc71de3cd3f8a44cbaf85"
     }
     
     if (len(sys.argv) == 1):
          res = generateBlockHash(header)
     else:
          data = '{"method": "getbestblockhash", "params": []}'
          url = "http://127.0.0.1:8332/"
          auth = HTTPBasicAuth("raspibolt", getpass.getpass('password'))
          response = requests.post(url, data = data, auth = auth )
          result = response.json()['result']
          
          data2 = json.dumps({"method": "getblockheader", "params": [result]})
          response2 = requests.post(url, data = data2, auth = auth )
          result2 = response2.json()['result']
          
          res = generateBlockHash(result2)
     
