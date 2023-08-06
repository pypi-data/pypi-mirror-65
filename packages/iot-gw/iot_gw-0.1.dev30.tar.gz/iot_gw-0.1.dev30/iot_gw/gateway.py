import time
import json
from flask import Flask, request
from .bridge.gcp import MqttBridge
from .device import DeviceManager

app = Flask(__name__)
bridge = None
device_manager = None
configuration = None

@app.route('/',methods = ['GET'])
def index():
    return 'OK'

@app.route('/device/<device_id>',methods = ['GET'])
def get_device(device_id):
    device = device_manager.get_device(device_id)
    return json.dumps(device.toJson())

@app.route('/device/<device_id>/attach', methods = ['POST'])
def attach(device_id):
    device = device_manager.get_device(device_id)
    response = bridge.attach(device_id,device.get_token(get_project_id()))
    return 'OK' if response is True else 'KO'

@app.route('/device/<device_id>/state', methods = ['POST'])
def publish_state(device_id):
    response = bridge.publish(json.dumps(request.json),device_id,'state')
    return 'OK' if response is True else 'KO' 

@app.route('/device/<device_id>/event', methods = ['POST'])
def publish_event(device_id):
    response = bridge.publish(json.dumps(request.json),device_id)
    return 'OK' if response is True else 'KO'

def run(config):
    global bridge, device_manager, configuration
    configuration = config
    bridge = MqttBridge(config['bridge'])
    device_manager = DeviceManager(config['storage'])
    bridge.connect()
    
    

def publish_event(device_id,event):
    pass

def publish_state(self,device_id,state):
    pass

def get_project_id():
    return configuration['bridge']['project_id'] 

