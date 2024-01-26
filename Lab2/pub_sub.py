#Creates a publisher and subscriber, and transmits the time to the subscriber, which
#then calcuates the delay of transmission after receiving a message


import paho.mqtt.client as mqtt
import numpy as np
import time

#Publisher

# 0. define callbacks - functions that run when events happen.
# The callback for when the client receives a CONNACK response from the server.
def on_connect_pub(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected Disconnect")
    else:
        print("Expected Disconnect")
# The default message callback.
# (won’t be used if only publishing, but can still exist)
        
# 1. create a client instance.
pub = mqtt.Client()

# add additional client options (security, certifications, etc.)
# many default options should be good to start off.
# add callbacks to client.
pub.on_connect = on_connect_pub
pub.on_disconnect = on_disconnect

# 2. connect to a broker using one of the connect*() functions.
# client.connect_async("test.mosquitto.org")
pub.connect_async("mqtt.eclipseprojects.io")

# 3. call one of the loop*() functions to maintain network traffic flow with the broker.
pub.loop_start()

#Subscriber

def on_connect_sub(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    client.subscribe("ece180d/test/turner", qos=1)

# Subscribing in on_connect() means that if we lose the connection and reconnect then subscriptions will be renewed.
# The callback of the client when it disconnects.
        
def on_message(client, userdata, message):
    delay = (time.time() - float(message.payload)) * 1000
    print("Received message, delay = " + str(delay) + " ms.")
    
#initialize subscriber client
sub = mqtt.Client()

#define events
sub.on_connect = on_connect_sub
sub.on_disconnect = on_disconnect
sub.on_message = on_message

#connect to broker
sub.connect_async("mqtt.eclipseprojects.io")

#start subscriber loop
sub.loop_start()

# 5. use publish() to publish messages to the broker.
# payload must be a string, bytearray, int, float or None.
print("Publishing...")
for i in range(10):
    pub.publish("ece180d/test/turner", time.time(), qos=1)
    time.sleep(1)

# 6. use disconnect() to disconnect from the broker.
pub.loop_stop()
sub.loop_stop()

pub.disconnect()
sub.disconnect()