# -*- coding: utf-8 -*-
#driwall.py

"""
Driwall Server
===========
Socks5 Proxy Backend
It uses Websocket API to receive datas with a chat app mask
"""

import os
import logging
import gevent
import socket
import json
import struct
from flask import Flask
from flask_sockets import Sockets

app = Flask(__name__)
#app.debug = 'DEBUG' in os.environ

sockets = Sockets(app)

def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = ''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data
sockets_pool = {}
@app.route('/')
def hello():
    return "Hello World!\n It's Working!"

@sockets.route('/driwall')
def inbox(ws):
    """Receives incoming chat messages, inserts them into Redis."""
    
    while ws.socket is not None:
        # Sleep to prevent *contstant* context-switches.
        gevent.sleep(0.1)
        message = ws.receive()
        

        if message:

            msg = json.loads(message)
            if(msg["cmd"] == "connect"):

                sockets_pool["hl"+str(msg["HandlerId"])+"so"+str(msg["socketId"])] = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                sockets_pool["hl"+str(msg["HandlerId"])+"so"+str(msg["socketId"])].connect((msg["addr"]["dst"],msg["addr"]["port"]))
                data = sockets_pool["hl"+str(msg["HandlerId"])+"so"+str(msg["socketId"])].getsockname()
                obj = {'cmd':'connect','HandlerId':msg["HandlerId"],'socketId':msg["socketId"],'bnd':{'addr':data[0],'port':data[1]}}
                ws.send (json.dumps(obj))
                del data
            else:    

                send_msg(sockets_pool["hl"+str(msg["HandlerId"])+"so"+str(msg["socketId"])],jsoncontent[data])
                resp = recv_msg(sockets_pool["hl"+str(msg["HandlerId"])+"so"+str(msg["socketId"])])
                sockets_pool["hl"+str(msg["HandlerId"])+"so"+str(msg["socketId"])].close()
                obj = {'cmd':'resp','HandlerId':msg["HandlerId"],'socketId':msg["socketId"],'data':resp}
                ws.send (json.dumps(obj))