import paho.mqtt.client as mqtt
import numpy as np
import time
import keyboard

#Publisher

# 0. define callbacks - functions that run when events happen.
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    client.subscribe("ece180d/test/ahh/corwin", qos=1)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected Disconnect")
    else:
        print("Expected Disconnect")
# The default message callback.
# (won’t be used if only publishing, but can still exist)
                
def on_message(client, userdata, message):
    print("Received message, counter = " + str(int(message.payload)))
    new_num = int(message.payload) + 1

    time.sleep(1)
    print("Publishing new counter...")
    client.publish("ece180d/test/ahh/turner", new_num, qos=1)
        
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
client.connect_async("mqtt.eclipseprojects.io")

# 3. call one of the loop*() functions to maintain network traffic flow with the broker.
client.loop_start()

# 5. use publish() to publish messages to the broker.
# payload must be a string, bytearray, int, float or None.
while True:
    if keyboard.is_pressed('q'):
            print("Exiting the program.")
            break

# 6. use disconnect() to disconnect from the broker.
client.loop_stop()
client.disconnect()