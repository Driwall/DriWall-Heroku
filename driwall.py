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
            jsoncontent = json.loads(message)
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect((jsoncontent[addr][dst],jsoncontent[addr][port]))
            send_msg(s,jsoncontent[data])
            resp = recv_msg(s)
            s.close()
            obj = {'HandlerId':jsoncontent[HandlerId],'socketId':jsoncontent[socketId],'data':resp}
            ws.send (json.dumps(obj))