from flask import Flask
from flask import request
import logging

proxy=Flask(__name__)
proxy.on_attach=None
proxy.on_event=None
proxy.on_state=None

@proxy.route('/',methods=['GET'])
def __hello():
    return "Hello World 1"

@proxy.route('/attach/<device_id>',methods=['POST'])
def __attach(device_id):
    proxy.on_attach(device_id)

@proxy.route('/event/<device_id>',methods=['POST'])
def __event(device_id):
    proxy.on_event(device_id,request.json)

@proxy.route('/state/<device_id>',methods=['POST'])
def __event(device_id):
    proxy.on_state(device_id,request.json)
