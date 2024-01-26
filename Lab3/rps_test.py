import numpy as np
import paho.mqtt.client as mqtt
import time

# 0. define callbacks - functions that run when events happen.
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("ece180d/test/ahh/#", qos=1)

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
    if topics[-1] == 'server':
        print(str(message.payload))
        if (str(message.payload) == 'b\'Users play Rock (1), Paper (2), or Scissors (3)\''):
            move = input()
            while not(move == '1' or move == '2' or move == '3'):
                move = input()
            print("Sent move, awaiting response...")
            client.publish("ece180d/test/ahh/turner", str(move), qos=1)

# 1. create a client instance.
client = mqtt.Client()
# add additional client options (security, certifications, etc.)
# many default options should be good to start off.
# add callbacks to client.
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
# 2. connect to a broker using one of the connect*() functions.
# client.connect_async("test.mosquitto.org")
client.connect_async('mqtt.eclipseprojects.io')
# client.connect("test.mosquitto.org", 1883, 60)
# client.connect("mqtt.eclipse.org")
# 3. call one of the loop*() functions to maintain network traffic flow with the broker.
client.loop_start()
# client.loop_forever()
while(True):
    pass
# use subscribe() to subscribe to a topic and receive messages.
# use publish() to publish messages to the broker.
# use disconnect() to disconnect from the broker.

client.loop_stop()
client.disconnect()