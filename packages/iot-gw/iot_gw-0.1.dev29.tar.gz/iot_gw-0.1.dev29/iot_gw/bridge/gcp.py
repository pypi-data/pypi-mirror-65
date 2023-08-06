import time
import datetime
import json
import jwt
import ssl
import paho.mqtt.client as mqtt
import logging


"""
Bridge client for Google Cloud Platform
"""

def create_jwt_token(project_id,private_key_file,algorithm='RS256',minutes=60):
    token = {
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=minutes),
            'aud' : project_id
        }
    with open(private_key_file, 'r') as f:
        private_key = f.read()     
    return jwt.encode(token,private_key,algorithm=algorithm)

def create_mqtt_client(project_id,region,registry_id, device_id, private_key_file, ca_certs_file):
    client_id='projects/{}/locations/{}/registries/{}/devices/{}'.format(
            project_id,
            region,
            registry_id,
            device_id
        )
    client = mqtt.Client(client_id=client_id)
    client.username_pw_set(
        username = 'unused',
        password = create_jwt_token(project_id,private_key_file)
    )
    client.enable_logger(logging)
    client.tls_set(ca_certs =ca_certs_file, tls_version= ssl.PROTOCOL_TLSv1_2)
    return client

class MqttBridge:
    """
    MQTT bridge client for Google Cloud Platform 

    Configuration properties:
      - project_id
      - region
      - registry_id
      - device_id
      - private_key_file
      - ca_certs_file
      - bridge_hostname
      - bridge_port
    """
    def __init__(self,config):
        self.__is_connected=False
        self.__config=config
        self.__client=create_mqtt_client(
            config['project_id'],
            config['region'],
            config['registry_id'],
            config['device_id'],
            config['private_key_file'],
            config['ca_certs_file']
        )
        self.__client.on_connect = self.__on_connect
        self.__client.on_disconnect = self.__on_disconnect
        self.__client.on_message = self.__on_message
    
    def connect(self):
        self.__client.connect_async(
            self.__config['bridge_hostname'],
            self.__config['bridge_port']
        )
        self.__client.loop_start()
        self.__wait_for_connection(timeout=5)

    def attach(self,device_id,jwt_token=None):
        print(jwt_token)
        print(jwt_token.decode('utf-8'))
        payload = json.dumps({"authorization" : jwt_token.decode('utf-8')}) if jwt_token is not None else None
        return self.publish(payload,device_id,'attach',1)
            
    def publish(self,payload,device_id=None,type='events',qos=0):
        if not self.__is_connected:
            self.connect()
        result = self.__client.publish(
            topic="/devices/{}/{}".format(device_id if device_id != None else self.config['device_id'],type),
            payload=payload,
            qos=qos) 
        result.wait_for_publish()
        return result.is_published()

    def is_connected(self):
        return self.__is_connected

    def __wait_for_connection(self, timeout=5):
        total_time = 0
        while not self.__is_connected and total_time < timeout:
            logging.debug("wait_for_connection %d" % timeout)
            if timeout > 0:
                total_time +=1
            time.sleep(1)
        if not self.__is_connected:
            raise RuntimeError('Could not connect to MQTT bridge.')
        logging.debug("wait_for_connection terminated %s" % self.is_connected)
        
    def __on_connect(self,client,userdata,flags,rc):
        logging.debug("MQTT bridge connection is up")
        self.__is_connected=True
        self.__client.subscribe('/devices/{}/config'.format(self.__config['device_id']), qos=1)
        self.__client.subscribe('/devices/{}/errors'.format(self.__config['device_id']), qos=0)

    def __on_disconnect(self,client,userdate,rc):
        logging.debug("MQTT bridge connection is down")
        self.__is_connected=False

    def __on_message(self, client, userdata, message):
        payload = str(message.payload.decode('utf-8'))
        logging.debug(
            'Received message \'{}\' on topic \'{}\' with Qos {}'
            .format(payload, message.topic, str(message.qos))
        )
    

    
    
