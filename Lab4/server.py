#Code from last lab, with only changes in naming convention etc.

import paho.mqtt.client as mqtt
import time

# 0. define callbacks - functions that run when events happen.
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("ece180d/test/ahh/client", qos=1)
    client.publish("ece180d/test/ahh/server", '1', qos=1)

# The callback of the client when it disconnects.
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')
              
# The default message callback.
# (you can create separate callbacks per subscribed topic)
def on_message(client, userdata, message):
    topics = message.topic.split('/')
    if topics[-1] != 'server':
        print('Received message: \"' + str(message.payload) + '\" on topic \"' + message.topic + '\" with QoS ' + str(message.qos))
        next_val = int(message.payload)+1
        time.sleep(1)
        print('Sent message: \"' + str(next_val) + '\" on topic \"' + "ece180d/test/ahh/server" + '\" with QoS ' + str(message.qos))
        client.publish("ece180d/test/ahh/server", str(next_val), qos=1)

# 1. create a client instance.
client = mqtt.Client()

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
# 2. connect to a broker using one of the connect*() functions.

client.connect_async('mqtt.eclipseprojects.io')

# 3. call one of the loop*() functions to maintain network traffic flow with the broker.

client.loop_start()

while True:
    pass

client.loop_stop()
client.disconnect()