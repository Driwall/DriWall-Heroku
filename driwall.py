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
import thread 
from time import sleep
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

def heart_beats:
    obj = json.dumps({'cmd':'ping'})
    while true:
        ws.send(obj)
        sleep(45)

def DriWall_req(message):
    msg = json.loads(message)

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((msg["dst"]["addr"],msg["dst"]["port"]))
    send_msg(s,msg["data"])
    resp = recv_msg(s)
    obj = {'cmd':'resp','HandlerId':msg["HandlerId"],'socketId':msg["socketId"],'data':resp}
    ws.send (json.dumps(obj))
    s.close()

@app.route('/')
def hello():
    return "Hello World!\n It's Working!"

@sockets.route('/driwall')
def inbox(ws):
    
    thread.start_new_thread(heart_beats,())
    
    while ws.socket is not None:
        # Sleep to prevent *contstant* context-switches.
        gevent.sleep(0.1)
        message = ws.receive()
        

        if message:

            thread.start_new_thread(DriWall_req,(message,))
            
                