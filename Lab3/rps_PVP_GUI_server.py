import paho.mqtt.client as mqtt
import time

#define MQTT functions

def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    client.subscribe("ece180d/test/ahh/client1", qos=1)
    client.subscribe("ece180d/test/ahh/client2", qos=1)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected Disconnect")
    else:
        print("Expected Disconnect")

#globals
client_1_score = 0
client_2_score = 0

client_1_move = 'n'
client_2_move = 'n'

running = True

#takes in r,p,s as char, and returns 0,1,2 as int
def convert_move(move):
    if (move == 'r'):
        return 0
    elif (move == 'p'):
        return 1
    else:
        return 2


#takes in player moves, determines the winner, and updates score variables
#returns 0 if a tie, 1 if player 1 wins, and 2 if player 2 wins
def play_rps(move1, move2):
    global client_1_score
    global client_2_score

    move1 = convert_move(move1)
    move2 = convert_move(move2)
    print(move1)
    print(move2)

    diff = (move1 - move2) % 3

    if (diff == 0):  #tie
        return '0'
    elif (diff == 1):  #player 1 win
        client_1_score += 1
        return '1'
    else:  #player 2 win
        client_2_score += 1
        return '2'

def on_message(client, userdata, message):
    global client_1_move
    global client_2_move
    global running

    payload = message.payload.decode()

    if (payload[1] == 'q'):
        running = False

    if (payload[0] == '1'):  #from client 1
        print("Received move from client 1")
        client_1_move = payload[1]
    else:  #from client 2
        print("Received move from client 2")
        client_2_move = payload[1]

    if (client_1_move != 'n' and client_2_move > 'n'):  #both players have moved
        #calculate result
        result = play_rps(client_1_move, client_2_move)

        #reset move state
        client_1_move = 'n'
        client_2_move = 'n'

        #publish result
        client.publish("ece180d/test/ahh/server1", result, qos=1)
        client.publish("ece180d/test/ahh/server2", result, qos=1)
        print("Published results...")
    

#create MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.connect_async("mqtt.eclipseprojects.io")
client.loop_start()

while running:
    pass

client.loop_stop()
client.disconnect()