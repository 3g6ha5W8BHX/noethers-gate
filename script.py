#!/usr/bin/python2.7

import sys
import json
import base64
import datetime
import xmlrpclib

import requests


# relay address, local BM rpc daemon
BM_RELAY_ADDR = "BM-2cVrx5dDYQJR5hDmnEKiA25pqJtQmAwxzg"
BM_SERVER = "http://username:password@127.0.0.1:8442/"

data = {"jsonrpc": "2.0", "id": "0"}
header = {"Content-Type": "application/json"}

# https://moneroworld.com/#nodes
monero_nodes = [
    "http://173.199.115.251:18089",
    "http://99.252.185.182:18089",
    "http://91.177.166.177:18089",
    "http://174.109.234.150:18089",
    "http://91.121.57.211:18089",
    "http://108.61.251.120:18089",
    "http://46.105.170.24:18089",
    "http://138.197.164.125:18089"
]

def send_raw_transaction(tx_as_hex):
    data = {}
    data["tx_as_hex"] = tx_as_hex
    data["do_not_relay"] = False
    dataEncoded = json.dumps(data)
    ret = []
    for url in monero_nodes:
        try:
          response = requests.post(
              url + "/send_raw_transaction", data=dataEncoded, headers=header)
          ret.append(response.json())
        except Exception as e:
            pass
    return ret

def gate():
    try:
        api = xmlrpclib.ServerProxy(BM_SERVER)
        inbox = json.loads(api.getAllInboxMessages())

        for msg in inbox['inboxMessages']:
            try:
                msgid = str(msg['msgid'])
                senders_address = str(msg['fromAddress'])
                to_address = str(msg['toAddress'])

                if to_address in BM_RELAY_ADDR:
                    subject = base64.b64decode(msg['subject'])
                    body = base64.b64decode(msg['message'])
                    
                    # TODO: do we have a transaction? check hex structure
                    # send msg body to nodes
                    ret  = send_raw_transaction(body)

                    # cleanup
                    api.trashMessage(msgid)
            except Exception as e:
                api.trashMessage(msgid)
    except Exception as e:
        # TODO: log error
        sys.exit()

def main():
    try:
        arg = sys.argv[1]

        if arg == "newMessage":
            gate()
            sys.exit()
        elif arg == "startingUp":
            sys.exit()
        elif arg == "newBroadcast":
            sys.exit()
        elif arg == "initalize":
            sys.exit()
        else:
            sys.exit()
    except Exception as e:
        print e
        sys.exit(0)

if __name__ == "__main__":
    main()
