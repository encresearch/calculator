import os, time
import paho.mqtt.client as mqtt
import pandas as pd
import numpy as np
from datetime import datetime
from influxdb import DataFrameClient

#Declaring Global Variables
HOST = "10.128.189.236"
PORT = 1883
KEEPALIVE = 120

#MQTT Topic to communicate with Notifier
topic =  "communication/influxdbUpdate"
#MQTT Client ID to remain unique
client_id = "/Calculator"


def connect_to_broker(client_id, host, port, keepalive, on_connect, on_message):
    ''' Params -> Client(client_id=””, clean_session=True, userdata=None, protocol=MQTTv311, transport=”tcp”)
    We set clean_session False, so in case connection is lost, it'll reconnect with same ID '''
    client = mqtt.Client(client_id=client_id, clean_session=False)
    client.on_connect = on_connect
    client.on_message = on_message
    connection = client.connect(host, port, keepalive)
    return (client, connection)


def main():
    '''
    Comment
    '''

    def on_connect(client, userdata, flags, rc):
        if rc==0:
            print(f"Connected OK: {client}")
            client.subscribe(topic, 2)
        else:
            print(f"Bad Connection Returned (Code: {rc})")
        pass

    def on_message(client, userdata, message):
        # Function for clients's specific callback when pubslishing message
        print(f"{message.payload.decode()}")
        pass

    #Establish Connection to the MQTT Broker
    client, connection = connect_to_broker(client_id=client_id, host=HOST, port=PORT, keepalive=KEEPALIVE, on_connect=on_connect, on_message=on_message)
    
    #Begin the connection loop, where within the loop, messages can be sent
    client.loop_forever()








if __name__ == "__main__":
    main()
