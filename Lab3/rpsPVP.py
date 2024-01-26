import paho.mqtt.client as mqtt
import numpy as np
import keyboard

def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    client.subscribe("ece180d/test/ahh/server", qos=1)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected Disconnect")
    else:
        print("Expected Disconnect")
                
def on_message(client, userdata, message):
    print(message.payload())
    player_move = input().lower()
    client.publish("ece180d/test/ahh/turner", player_move, qos=1)
    print("Move sent! Awaiting response...")
        
client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.connect_async("mqtt.eclipseprojects.io")
client.loop_start()

player_wins = 0
computer_wins = 0

print("Hello! Welcome to Rock Paper Scissors.")

while True:
    if keyboard.is_pressed('q'):
            print("Exiting the program.")
            break

client.loop_stop()
client.disconnect()